# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: msgs.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import (
    descriptor as _descriptor,
    descriptor_pool as _descriptor_pool,
    runtime_version as _runtime_version,
    symbol_database as _symbol_database,
)
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 29, 0, "", "msgs.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\nmsgs.proto\x12\x04msgs\x1a\x1cgoogle/protobuf/struct.proto"D\n\rInsertRequest\x12\x0c\n\x04path\x18\x01 \x01(\t\x12%\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct" \n\x0eInsertResponse\x12\x0e\n\x06status\x18\x01 \x01(\t2Q\n\x16\x44\x61talakeManagerService\x12\x37\n\nInsertData\x12\x13.msgs.InsertRequest\x1a\x14.msgs.InsertResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "msgs_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_INSERTREQUEST"]._serialized_start = 50
    _globals["_INSERTREQUEST"]._serialized_end = 118
    _globals["_INSERTRESPONSE"]._serialized_start = 120
    _globals["_INSERTRESPONSE"]._serialized_end = 152
    _globals["_DATALAKEMANAGERSERVICE"]._serialized_start = 154
    _globals["_DATALAKEMANAGERSERVICE"]._serialized_end = 235
# @@protoc_insertion_point(module_scope)
