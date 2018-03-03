#!/usr/bin/env python
##
# helpers.py
# collection of classes with various functions for
# every day tasks that I find useful. I put them all
# in one place so I can either copy-paste or just import
# specific classes from this library when I need them.
#
# author: adam m. swanda (deadbits.org)
# https://github.com/deadbits/py-potential
##

import os
import math
import zlib
import hmac
import hashlib
import shlex
import magic
import functools
import warnings
import psutil

from base64 import b64decode
from base64 import b64encode

from datetime import datetime
from decimal import Decimal

from subprocess import Popen
from subprocess import PIPE

from threading import Thread


class PathError(Exception):
    pass


@functools.wraps
def ignore_warnings(function):
    """ Decorator to ignore urllib warnings that annoy me """
    def _ignore_warning(*args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            result = function(*args, **kwargs)
        return result
    return _ignore_warning


@functools.wraps
def threaded(func):
    """ Decorator to be added to any function you want to run as a thread"""
    def _threaded(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return _threaded


class Time:
    """ Just get UTC times.. pretty straight forward """

    @staticmethod
    def utc_now_string():
        return datetime.isoformat(datetime.utcnow())


    @staticmethod
    def utc_now():
        return datetime.utcnow()


class System:
    """ Perform basic system tasks """

    @staticmethod
    def is_running(process_id):
        try:
            proc = psutil.Process(process_id)
            return proc.is_running()
        except psutil.NoSuchProcess:
            return False


    @staticmethod
    def proc_threads(process_id):
        try:
            proc = psutil.Process(process_id)
            return proc.threads()
        except psutil.NoSuchProcess:
            return False

    @staticmethod
    def proc_children(process_id, recursive=False):
        try:
            proc = psutil.Process(process_id)
            return proc.children(recursive)
        except psutil.NoSuchProcess:
            return False


    @staticmethod
    def run_command(command, ret_stdout=True, ret_stderr=True):
        proc = Popen(shlex.split(command),
                stdout=PIPE,
                stderr=PIPE,
                universal_newlines=True,
                close_fds=True)
        stdout, stderr = proc.communicate()

        if proc.returncode != 0:
            raise Exception('\n'.join(['Execution failed (%s) return code: %s' % (command, proc.returncode), stderr or '']))

        if ret_stdout:
            if ret_stderr:
                return (stdout, stderr)
            return stdout
        return None


class Validate:
    """Attempt to validate different types of data"""

    @staticmethod
    def validate_string(data):
        accepted_chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-@.'
        if all(c in accepted_chars for c in data.strip()):
            return True
        return False


    @staticmethod
    def url(addr):
        if addr.startswith("http://") or addr.startswith("https://"):
            return addr
        else:
            return "http://%s" % addr


    @staticmethod
    def ipv4(addr):
        parts = addr.split(".")
        if len(parts) != 4:
            return False
        for item in parts:
            if not 0 <= int(item) <= 255:
                return False
        return True


class Encode:
    """High-level encoding/encryption like things"""

    @staticmethod
    def xor(data, key):
        result = ''
        for i in data:
            result += chr(ord(i) ^ key)
        return result


    @staticmethod
    def rc4_crypt(data, key):
        out = []
        x = 0
        box = range(256)
        for i in range(256):
            x = (x + box[i] + ord(key[i % len(key)])) % 256
            box[i], box[x] = box[x], box[i]

        x = 0
        y = 0

        for char in data:
            x = (x + 1) % 256
            y = (y + box[x]) % 256
            box[x], box[y] = box[y], box[x]
            out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))

        return ''.join(out)


    @staticmethod
    def b64_zlib_encode(data):
        return b64encode(zlib.compress(data + '\n'))


    @staticmethod
    def b64_zlib_decode(data):
        return b64decode(zlib.decompress(data + '\n'))


    @staticmethod
    def hmac_sha256_digest(msg, key):
        return hmac.new(key, msg, hashlib.sha256).digest()


    @staticmethod
    def b64_encode(data):
        return b64encode(data)


    @staticmethod
    def b64_decode(data):
        return b64decode(data)



class Files:
    """Do things with files and their data"""

    @staticmethod
    def get_entropy(_buffer):
        """ Get entropy of a file or raw data.

        The _buffer argument assumes that if it's length is greater
        than 75, the input is a buffer. Otherwise it's treated as a file.
        """
        if len(_buffer) == 0:
            return Decimal(0)

        if len(_buffer) < 75:
            if not os.path.exists(_buffer):
                raise PathError('No file %s exists' % _buffer)

        data = open(_buffer, 'rb').read()

        entropy = Decimal(0)
        for x in range(256):
            p_x = Decimal(x) / len(data)
            entropy -= p_x * Decimal(math.log(p_x, 2))

        return entropy


    @staticmethod
    def is_valid(file_path):
        if os.path.exists(file_path) and os.path.isfile(file_path) \
                and os.path.getsize(file_path) > 0:
            return True
        return False


    @staticmethod
    def write(file_path, data):
        with open(file_path, 'w') as fp:
            fp.write(data)


    @staticmethod
    def read(file_path, lines=False):
        data = None
        if lines:
            data = (open(file_path, 'rb').read()).split('\n')
        else:
            data = open(file_path, 'rb').read()
        return data


    @staticmethod
    def base_name(file_path):
        return os.path.base_name(file_path)


    @staticmethod
    def get_size(file_path):
        return os.path.getsize(file_path)


    @staticmethod
    def magic_buffer(data):
        result = ''
        try:
            with magic.Magic(flags=magic.MAGIC_MIME) as m:
                result = m.id_buffer(data)
        except:
            pass
        return result
