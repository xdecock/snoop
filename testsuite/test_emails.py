from snoop import models, emails

MAIL_PATH_MAPBOX = "eml-1-promotional/Introducing Mapbox Android Services - " \
              "Mapbox Team <newsletter@mapbox.com> - 2016-04-20 1603.eml"
MAIL_PATH_CODINGAME = "eml-1-promotional/New on CodinGame: Check it out! - " \
                 "CodinGame <coders@codingame.com> - 2016-04-21 1034.eml"
MAIL_PATH_CAMPUS = "eml-2-attachment/FW: Invitation Fontys Open Day 2nd " \
                    "of February 2014 - Campus Venlo " \
                    "<campusvenlo@fontys.nl> - 2013-12-16 1700.eml"
MAIL_PATH_AMERICAN = "eml-3-uppercaseheaders/Fwd: The American College " \
                     "of Thessaloniki - Greece - Tarek Kouatly " \
                     "<tarek@act.edu> - 2013-11-11 1622.eml"
MAIL_PATH_LONG_FILENAMES = "eml-5-long-names/Attachments have " \
                           "long file names..eml"
MAIL_PATH_NO_SUBJECT = "eml-2-attachment/message-without-subject.eml"
MAIL_PATH_OCTET_STREAM_CONTENT_TYPE = "eml-2-attachment/attachments-have-" \
                                      "octet-stream-content-type.eml"

MAIL_PATH_DOUBLE_DECODE_ATTACHMENT_FILENAME = "eml-8-double-encoded/double-" \
                                              "encoding.eml"

MAIL_PATH_BYTE_ORDER_MARK = "eml-bom/with-bom.eml"

def parse_email(path, collection):
    doc = models.Document(
        path=path,
        content_type='message/rfc822',
        collection=collection
    )
    return emails.parse_email(doc)

def test_subject(document_collection):
    data = parse_email(MAIL_PATH_MAPBOX, document_collection)
    assert data['subject'] == "Introducing Mapbox Android Services"

def test_no_subject_or_text(document_collection):
    data = parse_email(MAIL_PATH_NO_SUBJECT, document_collection)

    assert 'subject' in data
    assert len(data['subject']) == 0
    assert type(data['subject']) is str

    text = data['text']
    assert type(text) is str
    assert len(text) <= 2

def test_text(document_collection):
    data_codin = parse_email(MAIL_PATH_CODINGAME, document_collection)
    assert data_codin['text'].startswith("New on CodinGame: Check it out!")

    data_mapbox = parse_email(MAIL_PATH_MAPBOX, document_collection)
    assert "Android Services includes RxJava" in data_mapbox['text']

def test_people(document_collection):
    data = parse_email(MAIL_PATH_MAPBOX, document_collection)

    assert type(data['to']) is list
    assert len(data['to']) == 1
    assert "penultim_o@yahoo.com" in data['to']

    assert type(data['from']) is str
    assert "newsletter@mapbox.com" in data['from']

def test_normal_attachments(document_collection):
    data = parse_email(MAIL_PATH_CAMPUS, document_collection)
    attachments = data['attachments']

    assert attachments
    assert type(attachments) is dict
    assert len(attachments) == 2

def test_attachment_with_long_filename(document_collection):
    data = parse_email(MAIL_PATH_LONG_FILENAMES, document_collection)
    attachments = data['attachments']

    assert len(attachments) == 3

def test_tree_without_attachments(document_collection):
    data = parse_email(MAIL_PATH_MAPBOX, document_collection)
    tree = data['tree']

    assert set(tree.keys()) == {'headers', 'parts'}
    assert len(tree['parts']) == 2

    headers = {'subject', 'to', 'from', 'date', 'content-type'}
    assert headers.issubset(set(tree['headers'].keys()))

def test_tree_with_attachments(document_collection):
    data = parse_email(MAIL_PATH_LONG_FILENAMES, document_collection)
    tree = data['tree']

    assert set(tree.keys()) == {'headers', 'parts'}
    assert len(data['attachments']) == 3
    assert len(tree['parts']) == 4

    headers = {'subject', 'to', 'from', 'date', 'content-type'}
    assert headers.issubset(set(tree['headers'].keys()))

    for part in tree['parts']:
        assert 'headers' in part.keys()

def test_double_decoding_of_attachment_filenames(document_collection):
    data = parse_email(MAIL_PATH_DOUBLE_DECODE_ATTACHMENT_FILENAME, document_collection)
    without_encoding = "atașament_pârș.jpg"
    simple_encoding = "=?utf-8?b?YXRhyJlhbWVudF9ww6JyyJkuanBn?="
    double_encoding = "=?utf-8?b?PT91dGYtOD9iP1lYUmh5S" \
                      "mxoYldWdWRGOXd3Nkp5eUprdWFuQm4/PQ==?="

    filenames = [at[1]['filename'] for at in data.get('attachments').items()]
    assert double_encoding not in filenames
    assert {simple_encoding, without_encoding} == set(filenames)

def test_attachment_with_octet_stream_content_type(document_collection):
    data = parse_email(MAIL_PATH_OCTET_STREAM_CONTENT_TYPE, document_collection)

    assert data['attachments']['2']['content_type'] == 'application/msword'
    assert data['attachments']['3']['content_type'] == 'application/zip'
    assert data['attachments']['4']['content_type'] == 'image/png'

def test_email_with_byte_order_mark(document_collection):
    data = parse_email(MAIL_PATH_BYTE_ORDER_MARK, document_collection)

    assert data['subject'] == "xxxxxxxxxx"
    assert data['from'] == 'yyy <yyyyyyyyyyyyyyy@gmail.com>'
    assert 'YYYYYY YYYYY <xxxxxxxxxxxxxxx@gmail.com>' in data['to']