from app import app, db, queue_client
from datetime import datetime
from app.models import Attendee, Conference, Notification
from flask import render_template, session, request, redirect, url_for, flash, make_response, session
from azure.servicebus import Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/Registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        attendee = Attendee()
        attendee.first_name = request.form['first_name']
        attendee.last_name = request.form['last_name']
        attendee.email = request.form['email']
        attendee.job_position = request.form['job_position']
        attendee.company = request.form['company']
        attendee.city = request.form['city']
        attendee.state = request.form['state']
        attendee.interests = request.form['interest']
        attendee.comments = request.form['message']
        attendee.conference_id = app.config.get('CONFERENCE_ID')

        try:
            db.session.add(attendee)
            db.session.commit()
            session['message'] = 'Thank you, {} {}, for registering!'.format(attendee.first_name, attendee.last_name)
            return redirect('/Registration')
        except:
            logging.error('Error occured while saving your information')

    else:
        if 'message' in session:
            message = session['message']
            session.pop('message', None)
            return render_template('registration.html', message=message)
        else:
             return render_template('registration.html')

@app.route('/Attendees')
def attendees():
    attendees = Attendee.query.order_by(Attendee.submitted_date).all()
    return render_template('attendees.html', attendees=attendees)


@app.route('/Notifications')
def notifications():
    notifications = Notification.query.order_by(Notification.id).all()
    return render_template('notifications.html', notifications=notifications)

@app.route('/Notification', methods=['POST', 'GET'])
def notification():
    if request.method == 'POST':
        notification = Notification()
        notification.message = request.form['message']
        notification.subject = request.form['subject']
        notification.status = 'Notifications submitted'
        notification.submitted_date = datetime.utcnow()

        try:
            db.session.add(notification)
            db.session.commit()

            try:
                # Create a message containing the notification ID
                message = Message(str(notification_id))
                logging.error('log send queue')
                
                # Send the message to the queue
                with queue_client.get_sender() as sender:
                    sender.send_messages(message)
                
                print(f"Notification ID {notification_id} enqueued successfully.")
            except Exception as e:
                 print(f"Failed to enqueue notification ID {notification_id}: {e}")
            logging.error('log send queue ok')

            attendees = Attendee.query.all()

            for attendee in attendees:
                subject = '{}: {}'.format(attendee.first_name, notification.subject)
                send_email(attendee.email, subject, notification.message)

            notification.completed_date = datetime.utcnow()
            notification.status = 'Notified {} attendees'.format(len(attendees))
            db.session.commit()
            # TODO: Call servicebus queue_client to enqueue notification ID
            try:
                # Create a message containing the notification ID
                message = Message(str(notification_id))

                # Send the message to the queue
                with queue_client.get_sender() as sender:
                    sender.send_messages(message)
                
                print(f"Notification ID {notification_id} enqueued successfully.")
            except Exception as e:
                print(f"Failed to enqueue notification ID {notification_id}: {e}")
                return redirect('/Notifications')
            except :
                logging.error('log unable to save notification')

            return redirect('/Notifications')
        except :
            logging.error('log unable to save notification')
            return render_template('notification.html')


    else:
        return render_template('notification.html')

@app.route('/pushNotification', methods=['POST'])
def pushNotification():
        notification = Notification()
        notification.message = request.form['message']
        notification.subject = request.form['subject']
        notification.status = 'Notifications submitted'
        notification.submitted_date = datetime.utcnow()

        try:
            db.session.add(notification)
            db.session.commit()

            # Create a message containing the notification ID
            message = Message(str(notification.id))
            logging.info(f'log send queue {message}')
            logging.info(f'log send queue {notification.id}')
            
            # Send the message to the queue
            with queue_client.get_sender() as sender:
                sender.send(message)
            
            print(f"Notification ID {notification.id} enqueued successfully.")
            logging.info('log send queue done')

            attendees = Attendee.query.all()
            logging.info('log ssave attendee')

            # for attendee in attendees:
            #     subject = '{}: {}'.format(attendee.first_name, notification.subject)
            #     logging.error('log send mail')
            # logging.info('log ssave attendee done')
            
            #     # send_email(attendee.email, subject, notification.message)

            # notification.completed_date = datetime.utcnow()
            # notification.status = 'Notified {} attendees'.format(len(attendees))
            # db.session.commit()
            # # TODO: Call servicebus queue_client to enqueue notification ID
            # try:
            #     # Create a message containing the notification ID
            #     logging.info('Call servicebus queue_client to enqueue notification ID')
            #     message = Message(str(notification.id))

            #     # Send the message to the queue
            #     with queue_client.get_sender() as sender:
            #         sender.send_messages(message)
                
            #     print(f"Notification ID {notification.id} enqueued successfully.")
            # except Exception as e:
            #     logging.error(e.__traceback__)
            #     logging.error(f"Failed to enqueue notification ID {notification.id}: {e}")
            #     return redirect('/Notifications')
            # except Exception as e:
            #     logging.error(e.__traceback__)
            #     logging.error('log unable to save notification v2')

            return redirect('/Notifications')
        except  Exception as e:
            logging.error(e)
            logging.error(e.__traceback__)
            logging.error('log unable to save notification v1')
            return render_template('notification.html')




# def send_email(email, subject, body):
    # if not app.config.get('SENDGRID_API_KEY'):
    #     message = Mail(
    #         from_email=app.config.get('ADMIN_EMAIL_ADDRESS'),
    #         to_emails=email,
    #         subject=subject,
    #         plain_text_content=body)

    #     sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
    #     sg.send(message)
