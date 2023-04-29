import grpc
import project_pb2_grpc as pb2_grpc
import project_pb2 as pb2

blogs = "no"

choise = input("If you want to search for a blogger write 'search'\nif you want to log in to write a blog write 'write' ")

if (choise == 'write'):

    class UnaryClient(object):
        
        def __init__(self):

            # instantiate a channel
            self.channel = grpc.insecure_channel('localhost:6000')
            
            # bind the client and the server
            self.stub = pb2_grpc.LogInServiceStub(self.channel)

        def get_url(self, message):
            
            message = pb2.CredentialsRequest(message=message)
            return self.stub.CheckLogIn(message)


    if __name__ == '__main__':
        client = UnaryClient()
        while True:
            name = input("username: ")
            pw = input("password: ")
            message = f"{name}, {pw}"

            result = client.get_url(message)

            if(result.logged == True):
                print('You have been logged in')
                break
            else:
                print('please try again')

elif (choise == 'search'):

    class ClientSearch(object):
        
        def __init__(self):
            # instantiate a channel
            self.channel = grpc.insecure_channel('localhost:5000')
            
            # bind the client and the server
            self.stub = pb2_grpc.SearcherServiceStub(self.channel)

        def searchOne(self, user):
            
            message = pb2.OneRequest(user=user)
            return self.stub.SearchOne(message)
        
        def searchView(self, message):
            
            message = pb2.ViewRequest(find=message)
            return self.stub.SearchView(message)


    if __name__ == '__main__':
        client = ClientSearch()
        one = input('Do you want to search one blogger or view all: (one/all) ')

        if (one == 'one'):
            name = input('Please write the blogger: ')
            reply = client.searchOne(name)
            
            if reply.find == False:
                print('No user "{}" found').format(reply.user)
                
            else:
                print('User found')
                blogs = input('Do you wish to see the blogs (yes/no) ')
                userHeader = reply.user
            
        elif (one == 'all'):
            
            replys = client.searchView(True)
            print('Bloggers in the system:')
            for reply in replys:
                print("\t", reply.user)
        

if blogs == ('yes' or "Yes"):

    class ReaderBlog(object):
        def __init__(self):

            # instantiate a channel
            self.channel = grpc.insecure_channel('localhost:7000')
            
            # bind the client and the server
            self.stub = pb2_grpc.readerStub(self.channel)

        def headers(self, userHead):
            
            message = pb2.HeadRequest(userHead=userHead)
            return self.stub.viewHeadlines(message)
        
        def blog(self, header):
            message = pb2.BlogRequest(head=header)
            return self.stub.showBlog(message)
        
        def comment(self, com, head):
            message = pb2.CommentRequest(comment=com, head=head)
            return self.stub.commentBlog(message)

    if __name__ == '__main__':
        client = ReaderBlog()

        replys = client.headers(userHeader)
        
        print("Headlines from {}".format(userHeader))
        for reply in replys:
            print("\t", reply.head)
        header = input('Do you wish to read one of them? (write the header/no) ')
        if header != 'no':
            reply = client.blog(header)
            print(reply.head, 'by', userHeader)
            print(reply.blog)
            com = input('Do you wish to comment (yes/no) ')        
        if com == "yes":
            comment = input("Please write the comment\n")
            response = client.comment(comment, header)
            if response.add == True:
                print('Comment added')

            


    