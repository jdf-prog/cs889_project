# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/compiler/plugin.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%google/protobuf/compiler/plugin.proto\x12\x18google.protobuf.compiler\x1a google/protobuf/descriptor.proto\"c\n\x07Version\x12\x14\n\x05major\x18\x01 \x01(\x05R\x05major\x12\x14\n\x05minor\x18\x02 \x01(\x05R\x05minor\x12\x14\n\x05patch\x18\x03 \x01(\x05R\x05patch\x12\x16\n\x06suffix\x18\x04 \x01(\tR\x06suffix\"\xcf\x02\n\x14\x43odeGeneratorRequest\x12(\n\x10\x66ile_to_generate\x18\x01 \x03(\tR\x0e\x66ileToGenerate\x12\x1c\n\tparameter\x18\x02 \x01(\tR\tparameter\x12\x43\n\nproto_file\x18\x0f \x03(\x0b\x32$.google.protobuf.FileDescriptorProtoR\tprotoFile\x12\\\n\x17source_file_descriptors\x18\x11 \x03(\x0b\x32$.google.protobuf.FileDescriptorProtoR\x15sourceFileDescriptors\x12L\n\x10\x63ompiler_version\x18\x03 \x01(\x0b\x32!.google.protobuf.compiler.VersionR\x0f\x63ompilerVersion\"\xb3\x03\n\x15\x43odeGeneratorResponse\x12\x14\n\x05\x65rror\x18\x01 \x01(\tR\x05\x65rror\x12-\n\x12supported_features\x18\x02 \x01(\x04R\x11supportedFeatures\x12H\n\x04\x66ile\x18\x0f \x03(\x0b\x32\x34.google.protobuf.compiler.CodeGeneratorResponse.FileR\x04\x66ile\x1a\xb1\x01\n\x04\x46ile\x12\x12\n\x04name\x18\x01 \x01(\tR\x04name\x12\'\n\x0finsertion_point\x18\x02 \x01(\tR\x0einsertionPoint\x12\x18\n\x07\x63ontent\x18\x0f \x01(\tR\x07\x63ontent\x12R\n\x13generated_code_info\x18\x10 \x01(\x0b\x32\".google.protobuf.GeneratedCodeInfoR\x11generatedCodeInfo\"W\n\x07\x46\x65\x61ture\x12\x10\n\x0c\x46\x45\x41TURE_NONE\x10\x00\x12\x1b\n\x17\x46\x45\x41TURE_PROTO3_OPTIONAL\x10\x01\x12\x1d\n\x19\x46\x45\x41TURE_SUPPORTS_EDITIONS\x10\x02\x42r\n\x1c\x63om.google.protobuf.compilerB\x0cPluginProtosZ)google.golang.org/protobuf/types/pluginpb\xaa\x02\x18Google.Protobuf.Compiler')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'google.protobuf.compiler.plugin_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.google.protobuf.compilerB\014PluginProtosZ)google.golang.org/protobuf/types/pluginpb\252\002\030Google.Protobuf.Compiler'
  _globals['_VERSION']._serialized_start=101
  _globals['_VERSION']._serialized_end=200
  _globals['_CODEGENERATORREQUEST']._serialized_start=203
  _globals['_CODEGENERATORREQUEST']._serialized_end=538
  _globals['_CODEGENERATORRESPONSE']._serialized_start=541
  _globals['_CODEGENERATORRESPONSE']._serialized_end=976
  _globals['_CODEGENERATORRESPONSE_FILE']._serialized_start=710
  _globals['_CODEGENERATORRESPONSE_FILE']._serialized_end=887
  _globals['_CODEGENERATORRESPONSE_FEATURE']._serialized_start=889
  _globals['_CODEGENERATORRESPONSE_FEATURE']._serialized_end=976
# @@protoc_insertion_point(module_scope)
