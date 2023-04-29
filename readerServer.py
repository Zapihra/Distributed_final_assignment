from concurrent import futures

import grpc
import project_pb2_grpc as pb2_grpc
import project_pb2 as pb2
import sqlite3

class Reader(pb2_grpc.readerServicer):

    def viewHeadlines(self, request, context):

        user = request.userHead

        con = sqlite3.connect("blogs_comments.db")
        cur = con.cursor()
        data = "SELECT header FROM Blogs WHERE blogger = '{}'".format(user)
        res = cur.execute(data)
        headers = res.fetchall()

        for header in headers:
            yield pb2.HeadResponse(head=header[0])
        return

    def showBlog(self, request, context):

        head = request.head

        con = sqlite3.connect("blogs_comments.db")
        cur = con.cursor()
        data = "SELECT blog FROM Blogs WHERE header = '{}'".format(head)
        res = cur.execute(data)
        blog = res.fetchone()

        return pb2.BlogResponse(head=head, blog=blog[0])
    
    def commentBlog(self, request, context):

        head = request.head
        com = request.comment
        con = sqlite3.connect("blogs_comments.db")
        cur = con.cursor()

        data = "SELECT BlogNumb FROM Blogs WHERE Header = '{}'".format(head)
        res = cur.execute(data)
        numb = res.fetchone()

        data = "INSERT INTO Comment (BlogNum, Comm) VALUES ({}, '{}')".format(numb[0], com)
        res = cur.execute(data)

        return pb2.CommentResponse(add=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_readerServicer_to_server(Reader(), server)
    server.add_insecure_port('localhost:7000')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()