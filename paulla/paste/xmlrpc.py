from pyramid_xmlrpc import XMLRPCView
from pyramid_xmlrpc import parse_xmlrpc_request
from pyramid_xmlrpc import xmlrpc_response


class XmlRPC(XMLRPCView):
    def  __call__(self):
        params, method = parse_xmlrpc_request(self.request)
        print params, method

        return xmlrpc_response(getattr(self,method)(*params))

    def newPaste(self, args1, args2, args3, args4, args5,  args6,pastebin_private):
        print args1, args2, args3, args4, args5,  args6,pastebin_private
        return ''



