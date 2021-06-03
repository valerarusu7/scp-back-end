from fpdf import FPDF
from pdf_mail import sendpdf
from filehash import FileHash
from pathlib import Path


def generate_pdf(json_data):
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.add_page()
    pdf.set_font('helvetica', 'BIU', 16)
    pdf.cell(120, 100, 'DIPLOMA - ' + json_data['education'], ln=True)
    pdf.set_font('times', '', 12)
    pdf.cell(80, 10, json_data['student_name'], ln=True)
    pdf.cell(120, 100, 'localhost:3000/validate/' + json_data['student_number'], ln=True)
    pdf.output(json_data['student_number'] + '.pdf')


def get_hash_of_pdf(file_path):
    sha256 = FileHash('sha256')
    return sha256.hash_file(file_path)


def send_email(json_data):
    sender_address = 'viatestemail2021@gmail.com'
    sender_pass = 'via2021!testemail'
    receiver_address = json_data['student_number'] + '@via.dk'
    path = Path(__file__).parent
    email = sendpdf(sender_address, receiver_address, sender_pass, 'Graduation Email',
                    'Congratulation for graduating from VIA University College, have a wonderful life!',
                    json_data['student_number'], path)
    email.email_send()
