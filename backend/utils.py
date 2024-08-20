import csv
from io import StringIO

def load_csv(csv_file):
    data = []
    csv_file = StringIO(csv_file)
    csv_reader = csv.reader(csv_file)
    headers = next(csv_reader)
    if headers[0] == "\ufeffZip":
        headers[0] = "Zip"
    for row in csv_reader:
        new_data = {header: value for header, value in zip(headers, row) if value}
        if new_data:  
            data.append(new_data)
    return data

def _extract_file(headers, body):
    multipart_string = base64.b64decode(body)
    content_type = headers['content-type']

    multipart_data = decoder.MultipartDecoder(
        multipart_string, content_type)

    filename = None
    part = multipart_data.parts[0]
    content = part.content
    disposition = part.headers[b'Content-Disposition']
    for content_info in str(disposition).split(';'):
        info = content_info.split('=', 2)
        if info[0].strip() == 'filename':
            filename = info[1].strip('\"\'\t \r\n')
    assert filename is not None
    file = {'file': (filename, content)}
    return file