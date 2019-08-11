"""
Author: Meng
Date: 2019/8/10
"""
import typing

import mitmproxy.addonmanager
import mitmproxy.connections
import mitmproxy.http
import mitmproxy.log
import mitmproxy.tcp
import mitmproxy.websocket
import mitmproxy.proxy.protocol
import change_host
import requests

port = 8080


class Events:
    # HTTP lifecycle
    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        """
            An HTTP CONNECT request was received. Setting a non 2xx response on
            the flow will return the response to the client abort the
            connection. CONNECT requests and responses do not generate the usual
            HTTP handler events. CONNECT requests are only valid in regular and
            upstream proxy modes.
        """

    def requestheaders(self, flow: mitmproxy.http.HTTPFlow):
        """
            HTTP request headers were successfully read. At this point, the body
            is empty.
        """

    def request(self, flow: mitmproxy.http.HTTPFlow):
        """
            The full HTTP request has been read.
        """



    def responseheaders(self, flow: mitmproxy.http.HTTPFlow):
        """
            HTTP response headers were successfully read. At this point, the body
            is empty.
        """

    def response(self, flow: mitmproxy.http.HTTPFlow):
        """
            The full HTTP response has been read.
        """
        ip = change_host.host_manage(flow.request.host, 8080)
        if ip:
            # flow.request.host = ip

            flow.request.scheme = 'http'
            proxies = {'http': f'http://{ip}',
                       'https': f'https://{ip}'}
            headers = change_host.to_dict(flow.request.headers)
            pdata = change_host.to_dict(flow.request.query)
            print(pdata)
            respnose = requests.request(flow.request.method,
                                        flow.request.url.replace('https:', 'http:'),
                                        data=pdata,
                                        headers=headers,
                                        timeout=2,
                                        verify=False,
                                        proxies=proxies,
                                        )

            flow.response.content = respnose.content
            print(f'change host: {ip}')

    def error(self, flow: mitmproxy.http.HTTPFlow):
        """
            An HTTP error has occurred, e.g. invalid server responses, or
            interrupted connections. This is distinct from a valid server HTTP
            error response, which is simply a response with an HTTP error code.
        """

    # TCP lifecycle
    def tcp_start(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP connection has started.
        """

    def tcp_message(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP connection has received a message. The most recent message
            will be flow.messages[-1]. The message is user-modifiable.
        """

    def tcp_error(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP error has occurred.
        """

    def tcp_end(self, flow: mitmproxy.tcp.TCPFlow):
        """
            A TCP connection has ended.
        """


addons = [
    Events()
]
