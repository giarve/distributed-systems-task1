# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: server.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='server.proto',
  package='server',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0cserver.proto\x12\x06server\x1a\x1bgoogle/protobuf/empty.proto\"\x14\n\x06Status\x12\n\n\x02ok\x18\x01 \x01(\x08\"\x16\n\x08WorkerId\x12\n\n\x02id\x18\x01 \x01(\r\"\x18\n\nWorkerList\x12\n\n\x02id\x18\x01 \x03(\r\"m\n\x08WorkType\x12)\n\x07program\x18\x01 \x01(\x0e\x32\x18.server.WorkType.Program\x12\x0c\n\x04urls\x18\x02 \x03(\t\"(\n\x07Program\x12\r\n\tWORDCOUNT\x10\x00\x12\x0e\n\nCOUNTWORDS\x10\x01\"\x13\n\x05JobId\x12\n\n\x02id\x18\x01 \x01(\t2\xdb\x01\n\x10WorkerManagement\x12\x32\n\x06\x63reate\x12\x16.google.protobuf.Empty\x1a\x0e.server.Status\"\x00\x12;\n\x0blistWorkers\x12\x16.google.protobuf.Empty\x1a\x12.server.WorkerList\"\x00\x12,\n\x06\x64\x65lete\x12\x10.server.WorkerId\x1a\x0e.server.Status\"\x00\x12(\n\x03job\x12\x10.server.WorkType\x1a\r.server.JobId\"\x00\x62\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])



_WORKTYPE_PROGRAM = _descriptor.EnumDescriptor(
  name='Program',
  full_name='server.WorkType.Program',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='WORDCOUNT', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='COUNTWORDS', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=194,
  serialized_end=234,
)
_sym_db.RegisterEnumDescriptor(_WORKTYPE_PROGRAM)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='server.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ok', full_name='server.Status.ok', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=53,
  serialized_end=73,
)


_WORKERID = _descriptor.Descriptor(
  name='WorkerId',
  full_name='server.WorkerId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='server.WorkerId.id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=75,
  serialized_end=97,
)


_WORKERLIST = _descriptor.Descriptor(
  name='WorkerList',
  full_name='server.WorkerList',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='server.WorkerList.id', index=0,
      number=1, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=99,
  serialized_end=123,
)


_WORKTYPE = _descriptor.Descriptor(
  name='WorkType',
  full_name='server.WorkType',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='program', full_name='server.WorkType.program', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='urls', full_name='server.WorkType.urls', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _WORKTYPE_PROGRAM,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=125,
  serialized_end=234,
)


_JOBID = _descriptor.Descriptor(
  name='JobId',
  full_name='server.JobId',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='server.JobId.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=236,
  serialized_end=255,
)

_WORKTYPE.fields_by_name['program'].enum_type = _WORKTYPE_PROGRAM
_WORKTYPE_PROGRAM.containing_type = _WORKTYPE
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.message_types_by_name['WorkerId'] = _WORKERID
DESCRIPTOR.message_types_by_name['WorkerList'] = _WORKERLIST
DESCRIPTOR.message_types_by_name['WorkType'] = _WORKTYPE
DESCRIPTOR.message_types_by_name['JobId'] = _JOBID
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:server.Status)
  })
_sym_db.RegisterMessage(Status)

WorkerId = _reflection.GeneratedProtocolMessageType('WorkerId', (_message.Message,), {
  'DESCRIPTOR' : _WORKERID,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:server.WorkerId)
  })
_sym_db.RegisterMessage(WorkerId)

WorkerList = _reflection.GeneratedProtocolMessageType('WorkerList', (_message.Message,), {
  'DESCRIPTOR' : _WORKERLIST,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:server.WorkerList)
  })
_sym_db.RegisterMessage(WorkerList)

WorkType = _reflection.GeneratedProtocolMessageType('WorkType', (_message.Message,), {
  'DESCRIPTOR' : _WORKTYPE,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:server.WorkType)
  })
_sym_db.RegisterMessage(WorkType)

JobId = _reflection.GeneratedProtocolMessageType('JobId', (_message.Message,), {
  'DESCRIPTOR' : _JOBID,
  '__module__' : 'server_pb2'
  # @@protoc_insertion_point(class_scope:server.JobId)
  })
_sym_db.RegisterMessage(JobId)



_WORKERMANAGEMENT = _descriptor.ServiceDescriptor(
  name='WorkerManagement',
  full_name='server.WorkerManagement',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=258,
  serialized_end=477,
  methods=[
  _descriptor.MethodDescriptor(
    name='create',
    full_name='server.WorkerManagement.create',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_STATUS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='listWorkers',
    full_name='server.WorkerManagement.listWorkers',
    index=1,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=_WORKERLIST,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='delete',
    full_name='server.WorkerManagement.delete',
    index=2,
    containing_service=None,
    input_type=_WORKERID,
    output_type=_STATUS,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='job',
    full_name='server.WorkerManagement.job',
    index=3,
    containing_service=None,
    input_type=_WORKTYPE,
    output_type=_JOBID,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WORKERMANAGEMENT)

DESCRIPTOR.services_by_name['WorkerManagement'] = _WORKERMANAGEMENT

# @@protoc_insertion_point(module_scope)
