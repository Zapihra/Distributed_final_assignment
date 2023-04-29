import grpc
from concurrent import futures
import sqlite3
import project_pb2_grpc as pb2_grpc
import project_pb2 as pb2


class LogInService(pb2_grpc.LogInService):

    def CheckLogIn(self, request, context):
        
        message = request.message
        print(message)
        split = message.split(', ')

        con = sqlite3.connect("pw_users.db")
        cur = con.cursor()
        data = "SELECT user, password FROM Users WHERE user = '{}'".format(split[0])
        res = cur.execute(data)
        user, pw = res.fetchone()

        if (split[1] == pw):
            
            resp = {'logged': True}
            return pb2.CredentialsResponse(**resp)
        else:
            
            resp = {'logged': False}
            return pb2.CredentialsResponse(**resp)
        
        
        

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_LogInServiceServicer_to_server(LogInService(), server)
    server.add_insecure_port('localhost:6000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()