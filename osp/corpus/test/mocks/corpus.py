

import os
import tempfile
import hashlib

from abc import ABCMeta
from reportlab.pdfgen.canvas import Canvas
from docx import Document


class MockCorpus:


    def __init__(self):

        """
        Create the temporary directory.
        """

        self.dir = tempfile.mkdtemp()


    def add_segment(self, name):

        """
        Add a segment directory.

        Args:
            name (str): The segment name.
        """

        path = os.path.join(self.dir, name)

        if not os.path.exists(path):
            os.makedirs(path)


    def add_file(self, segment, content, ftype='txt'):

        """
        Add a file to the corpus.

        Args:
            segment (str): The segment name.
            content (str): The file content.
            fname (str): The file name.
            ftype (str): The file type.
        """

        # Get the file cheksum.
        sha1 = hashlib.sha1()
        sha1.update(content.encode('utf8'))
        name = sha1.hexdigest()

        # Get the complete path.
        path = os.path.join(self.dir, segment+'/'+sha1.hexdigest())

        # Write the file.
        write_file = getattr(self, 'write_'+ftype)
        return write_file(path, content)


    def write_pdf(self, path, content):

        """
        Add a PDF file.

        Args:
            path (str): The file path.
            content (str): The file content.

        Returns:
            file: A handle on the new file.
        """

        canvas = Canvas(path)
        canvas.drawString(12, 720, content)
        canvas.save()

        return open(path, 'rb')


    def write_docx(self, path, content):

        """
        Add a .docx file.

        Args:
            path (str): The file path.
            content (str): The file content.

        Returns:
            file: A handle on the new file.
        """

        docx = Document()
        docx.add_paragraph(content)
        docx.save(path)

        return open(path, 'rb')
