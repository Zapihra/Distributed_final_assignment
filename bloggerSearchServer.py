from concurrent import futures

import grpc
import project_pb2_grpc as pb2_grpc
import project_pb2 as pb2
import sqlite3


class SearcherService(pb2_grpc.SearcherServiceServicer):

    def SearchOne(self, request, context):

        user = request.user
        con = sqlite3.connect("users.db")
        cur = con.cursor()
        data = "SELECT usr FROM User WHERE usr = '{}'".format(user)
        res = cur.execute(data)
        usr = res.fetchone()
        
        if usr != None:
            
            resp = {'user': usr[0], 'find': True}
            return pb2.OneResponse(**resp)
        else:

            resp = {'user': user, 'find': False}
            return pb2.OneResponse(**resp)

    def SearchView(self, request, context):

        con = sqlite3.connect("users.db")
        cur = con.cursor()
        data = "SELECT usr FROM User"
        res = cur.execute(data)
        usrs = res.fetchall()
        
        for usr in usrs:
            yield pb2.ViewResponse(user=usr[0])

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_SearcherServiceServicer_to_server(SearcherService(), server)
    server.add_insecure_port('localhost:5000')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()