# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: utils/grpc/weblog.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='utils/grpc/weblog.proto',
  package='weblog',
  syntax='proto3',
  serialized_options=b'Z\t./grpcapi',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17utils/grpc/weblog.proto\x12\x06weblog\x1a\x1cgoogle/protobuf/struct.proto2\x89\x02\n\x06Weblog\x12\x39\n\x05Unary\x12\x16.google.protobuf.Value\x1a\x16.google.protobuf.Value\"\x00\x12\x42\n\x0cServerStream\x12\x16.google.protobuf.Value\x1a\x16.google.protobuf.Value\"\x00\x30\x01\x12\x42\n\x0c\x43lientStream\x12\x16.google.protobuf.Value\x1a\x16.google.protobuf.Value\"\x00(\x01\x12<\n\x04\x42idi\x12\x16.google.protobuf.Value\x1a\x16.google.protobuf.Value\"\x00(\x01\x30\x01\x42\x0bZ\t./grpcapib\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_struct__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)


DESCRIPTOR._options = None

_WEBLOG = _descriptor.ServiceDescriptor(
  name='Weblog',
  full_name='weblog.Weblog',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=66,
  serialized_end=331,
  methods=[
  _descriptor.MethodDescriptor(
    name='Unary',
    full_name='weblog.Weblog.Unary',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    output_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ServerStream',
    full_name='weblog.Weblog.ServerStream',
    index=1,
    containing_service=None,
    input_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    output_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ClientStream',
    full_name='weblog.Weblog.ClientStream',
    index=2,
    containing_service=None,
    input_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    output_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='Bidi',
    full_name='weblog.Weblog.Bidi',
    index=3,
    containing_service=None,
    input_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    output_type=google_dot_protobuf_dot_struct__pb2._VALUE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_WEBLOG)

DESCRIPTOR.services_by_name['Weblog'] = _WEBLOG

# @@protoc_insertion_point(module_scope)