import unittest
from unittest.mock import MagicMock
from src.Honeypotclass import Honeypot


class TestHoneypot(unittest.TestCase):
    def setUp(self):
        self.honeypot = Honeypot(22, "127.0.0.1", "key/host_key.pem", "192.168.0.1", None)

    def test_check_channel_request(self):
        import paramiko

        kind = "session"
        chanid = 1
        result = self.honeypot.check_channel_request(kind, chanid)
        self.assertEqual(result, paramiko.OPEN_SUCCEEDED)

    def test_check_channel_shell_request(self):
        channel = MagicMock()
        result = self.honeypot.check_channel_shell_request(channel)
        self.assertTrue(result)

    def test_check_channel_pty_request(self):
        channel = MagicMock()
        term = "xterm"
        width = 80
        height = 24
        pixelwidth = 640
        pixelheight = 480
        modes = {}
        result = self.honeypot.check_channel_pty_request(
            channel, term, width, height, pixelwidth, pixelheight, modes
        )
        self.assertTrue(result)

    def test_check_channel_exec_request(self):
        channel = MagicMock()
        command = b"ls -l"
        result = self.honeypot.check_channel_exec_request(channel, command)
        self.assertTrue(result)

    def test_check_auth_password(self):
        import paramiko

        username = "testuser"
        password = "testpassword"
        result = self.honeypot.check_auth_password(username, password)
        self.assertEqual(result, paramiko.AUTH_FAILED)

    def test_get_allowed_auths(self):
        username = "testuser"
        result = self.honeypot.get_allowed_auths(username)
        self.assertEqual(result, "publickey,password, none")

    def test_check_auth_publickey(self):
        import paramiko

        username = "testuser"
        key = MagicMock()
        key.get_name.return_value = "ssh-rsa"
        key.get_base64.return_value = "AAAAB3NzaC1yc2EAAAADAQABAAABAQD..."
        result = self.honeypot.check_auth_publickey(username, key)
        self.assertEqual(result, paramiko.AUTH_FAILED)


if __name__ == "__main__":
    unittest.main()
