import paramiko
import unittest
from unittest.mock import MagicMock

import paramiko.ssh_exception


class TestHoneypot(unittest.TestCase):

    def test_handle_chan_no_channel(self):
        with self.assertRaises(paramiko.ssh_exception.SSHException):
            transport = paramiko.Transport(("127.0.0.1", 22))
            self.honeypot.handle_chan(transport, ("127.0.0.1", 12345))

