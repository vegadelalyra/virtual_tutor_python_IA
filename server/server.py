import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

users = {}


@sio.event
def connect(sid, environ):
    print(f'Client connected: {sid}')
    sio.emit('message', 'hello from server, human')


@sio.event
def disconnect(sid):
    if sid in users:
        user_name = users[sid]
        del users[sid]
        sio.emit('user-disconnected', user_name)
        print(f'Client disconnected: {sid}')


@sio.event
def send_chat_message(sid, message):
    user_name = users.get(sid, 'Anonymous')
    sio.emit('chat-message', {'message': message,
             'name': user_name}, skip_sid=sid)


if __name__ == '__main__':
    # Use your preferred WSGI server to run the application
    # For example, you can use eventlet or gevent
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', 3000)), app)
