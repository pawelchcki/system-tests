# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protos/apm_test_client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cprotos/apm_test_client.proto\"\xca\x02\n\rStartSpanArgs\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x14\n\x07service\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tparent_id\x18\x03 \x01(\x04H\x01\x88\x01\x01\x12\x15\n\x08resource\x18\x04 \x01(\tH\x02\x88\x01\x01\x12\x11\n\x04type\x18\x05 \x01(\tH\x03\x88\x01\x01\x12\x13\n\x06origin\x18\x06 \x01(\tH\x04\x88\x01\x01\x12\x32\n\x0chttp_headers\x18\x07 \x01(\x0b\x32\x17.DistributedHTTPHeadersH\x05\x88\x01\x01\x12\x1f\n\tspan_tags\x18\x08 \x03(\x0b\x32\x0c.HeaderTuple\x12\x1d\n\nspan_links\x18\t \x03(\x0b\x32\t.SpanLinkB\n\n\x08_serviceB\x0c\n\n_parent_idB\x0b\n\t_resourceB\x07\n\x05_typeB\t\n\x07_originB\x0f\n\r_http_headers\"<\n\x16\x44istributedHTTPHeaders\x12\"\n\x0chttp_headers\x18\x01 \x03(\x0b\x32\x0c.HeaderTuple\"y\n\x08SpanLink\x12\x13\n\tparent_id\x18\x01 \x01(\x04H\x00\x12/\n\x0chttp_headers\x18\x02 \x01(\x0b\x32\x17.DistributedHTTPHeadersH\x00\x12\x1f\n\nattributes\x18\x03 \x01(\x0b\x32\x0b.AttributesB\x06\n\x04\x66rom\")\n\x0bHeaderTuple\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"4\n\x0fStartSpanReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x10\n\x08trace_id\x18\x02 \x01(\x04\"$\n\x11InjectHeadersArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"Z\n\x13InjectHeadersReturn\x12\x32\n\x0chttp_headers\x18\x01 \x01(\x0b\x32\x17.DistributedHTTPHeadersH\x00\x88\x01\x01\x42\x0f\n\r_http_headers\"\x1c\n\x0e\x46inishSpanArgs\x12\n\n\x02id\x18\x01 \x01(\x04\"\x12\n\x10\x46inishSpanReturn\"\x14\n\x12SpanGetCurrentArgs\"9\n\x14SpanGetCurrentReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x10\n\x08trace_id\x18\x02 \x01(\x04\"\"\n\x0fSpanGetNameArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"!\n\x11SpanGetNameReturn\x12\x0c\n\x04name\x18\x01 \x01(\t\"&\n\x13SpanGetResourceArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\")\n\x15SpanGetResourceReturn\x12\x10\n\x08resource\x18\x01 \x01(\t\"/\n\x0fSpanGetMetaArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0b\n\x03key\x18\x02 \x01(\t\",\n\x11SpanGetMetaReturn\x12\x17\n\x05value\x18\x01 \x01(\x0b\x32\x08.AttrVal\"1\n\x11SpanGetMetricArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0b\n\x03key\x18\x02 \x01(\t\"$\n\x13SpanGetMetricReturn\x12\r\n\x05value\x18\x01 \x01(\x02\">\n\x0fSpanSetMetaArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\x13\n\x11SpanSetMetaReturn\"@\n\x11SpanSetMetricArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\x02\"\x15\n\x13SpanSetMetricReturn\"\x7f\n\x10SpanSetErrorArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x11\n\x04type\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x14\n\x07message\x18\x03 \x01(\tH\x01\x88\x01\x01\x12\x12\n\x05stack\x18\x04 \x01(\tH\x02\x88\x01\x01\x42\x07\n\x05_typeB\n\n\x08_messageB\x08\n\x06_stack\"\x14\n\x12SpanSetErrorReturn\"8\n\x13SpanSetResourceArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x10\n\x08resource\x18\x02 \x01(\t\"\x17\n\x15SpanSetResourceReturn\"@\n\x0fSpanAddLinkArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x1c\n\tspan_link\x18\x02 \x01(\x0b\x32\t.SpanLink\"\x13\n\x11SpanAddLinkReturn\"f\n\x0fHTTPRequestArgs\x12\x0b\n\x03url\x18\x01 \x01(\t\x12\x0e\n\x06method\x18\x02 \x01(\t\x12(\n\x07headers\x18\x03 \x01(\x0b\x32\x17.DistributedHTTPHeaders\x12\x0c\n\x04\x62ody\x18\x04 \x01(\x0c\"(\n\x11HTTPRequestReturn\x12\x13\n\x0bstatus_code\x18\x01 \x01(\t\"\x10\n\x0e\x46lushSpansArgs\"\x12\n\x10\x46lushSpansReturn\"\x15\n\x13\x46lushTraceStatsArgs\"\x17\n\x15\x46lushTraceStatsReturn\"\xfa\x02\n\x11OtelStartSpanArgs\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x16\n\tparent_id\x18\x03 \x01(\x04H\x00\x88\x01\x01\x12\x16\n\tspan_kind\x18\t \x01(\x04H\x01\x88\x01\x01\x12\x14\n\x07service\x18\x04 \x01(\tH\x02\x88\x01\x01\x12\x15\n\x08resource\x18\x05 \x01(\tH\x03\x88\x01\x01\x12\x11\n\x04type\x18\x06 \x01(\tH\x04\x88\x01\x01\x12\x16\n\ttimestamp\x18\x07 \x01(\x03H\x05\x88\x01\x01\x12\x1d\n\nspan_links\x18\x0b \x03(\x0b\x32\t.SpanLink\x12\x32\n\x0chttp_headers\x18\n \x01(\x0b\x32\x17.DistributedHTTPHeadersH\x06\x88\x01\x01\x12\x1f\n\nattributes\x18\x08 \x01(\x0b\x32\x0b.AttributesB\x0c\n\n_parent_idB\x0c\n\n_span_kindB\n\n\x08_serviceB\x0b\n\t_resourceB\x07\n\x05_typeB\x0c\n\n_timestampB\x0f\n\r_http_headers\"8\n\x13OtelStartSpanReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x10\n\x08trace_id\x18\x02 \x01(\x04\"C\n\x0fOtelEndSpanArgs\x12\n\n\x02id\x18\x01 \x01(\x04\x12\x16\n\ttimestamp\x18\x02 \x01(\x03H\x00\x88\x01\x01\x42\x0c\n\n_timestamp\"\x13\n\x11OtelEndSpanReturn\"%\n\x12OtelForceFlushArgs\x12\x0f\n\x07seconds\x18\x01 \x01(\r\"\'\n\x14OtelForceFlushReturn\x12\x0f\n\x07success\x18\x01 \x01(\x08\"%\n\x12OtelFlushSpansArgs\x12\x0f\n\x07seconds\x18\x01 \x01(\r\"\'\n\x14OtelFlushSpansReturn\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\x19\n\x17OtelFlushTraceStatsArgs\"\x1b\n\x19OtelFlushTraceStatsReturn\"\x14\n\x12OtelStopTracerArgs\"\x16\n\x14OtelStopTracerReturn\"&\n\x13OtelIsRecordingArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"-\n\x15OtelIsRecordingReturn\x12\x14\n\x0cis_recording\x18\x01 \x01(\x08\"&\n\x13OtelSpanContextArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"t\n\x15OtelSpanContextReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\t\x12\x10\n\x08trace_id\x18\x02 \x01(\t\x12\x13\n\x0btrace_flags\x18\x03 \x01(\t\x12\x13\n\x0btrace_state\x18\x04 \x01(\t\x12\x0e\n\x06remote\x18\x05 \x01(\x08\"\x18\n\x16OtelSpanGetCurrentArgs\"=\n\x18OtelSpanGetCurrentReturn\x12\x0f\n\x07span_id\x18\x01 \x01(\t\x12\x10\n\x08trace_id\x18\x02 \x01(\t\"G\n\x11OtelSetStatusArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\"\x15\n\x13OtelSetStatusReturn\"0\n\x0fOtelSetNameArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0c\n\x04name\x18\x02 \x01(\t\"\x13\n\x11OtelSetNameReturn\"I\n\x15OtelSetAttributesArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x1f\n\nattributes\x18\x02 \x01(\x0b\x32\x0b.Attributes\"\x19\n\x17OtelSetAttributesReturn\"4\n\x14OtelGetAttributeArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\x12\x0b\n\x03key\x18\x02 \x01(\t\"1\n\x16OtelGetAttributeReturn\x12\x17\n\x05value\x18\x01 \x01(\x0b\x32\x08.ListVal\"\"\n\x0fOtelGetNameArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\"!\n\x11OtelGetNameReturn\x12\x0c\n\x04name\x18\x01 \x01(\t\"#\n\x10OtelGetLinksArgs\x12\x0f\n\x07span_id\x18\x01 \x01(\x04\".\n\x12OtelGetLinksReturn\x12\x18\n\x05links\x18\x01 \x03(\x0b\x32\t.SpanLink\"r\n\nAttributes\x12*\n\x08key_vals\x18\x03 \x03(\x0b\x32\x18.Attributes.KeyValsEntry\x1a\x38\n\x0cKeyValsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x17\n\x05value\x18\x02 \x01(\x0b\x32\x08.ListVal:\x02\x38\x01\" \n\x07ListVal\x12\x15\n\x03val\x18\x01 \x03(\x0b\x32\x08.AttrVal\"g\n\x07\x41ttrVal\x12\x12\n\x08\x62ool_val\x18\x01 \x01(\x08H\x00\x12\x14\n\nstring_val\x18\x02 \x01(\tH\x00\x12\x14\n\ndouble_val\x18\x03 \x01(\x01H\x00\x12\x15\n\x0binteger_val\x18\x04 \x01(\x03H\x00\x42\x05\n\x03val\"\x10\n\x0eStopTracerArgs\"\x12\n\x10StopTracerReturn2\xf1\x0e\n\tAPMClient\x12/\n\tStartSpan\x12\x0e.StartSpanArgs\x1a\x10.StartSpanReturn\"\x00\x12\x32\n\nFinishSpan\x12\x0f.FinishSpanArgs\x1a\x11.FinishSpanReturn\"\x00\x12>\n\x0eSpanGetCurrent\x12\x13.SpanGetCurrentArgs\x1a\x15.SpanGetCurrentReturn\"\x00\x12\x35\n\x0bSpanGetName\x12\x10.SpanGetNameArgs\x1a\x12.SpanGetNameReturn\"\x00\x12\x41\n\x0fSpanGetResource\x12\x14.SpanGetResourceArgs\x1a\x16.SpanGetResourceReturn\"\x00\x12\x35\n\x0bSpanGetMeta\x12\x10.SpanGetMetaArgs\x1a\x12.SpanGetMetaReturn\"\x00\x12;\n\rSpanGetMetric\x12\x12.SpanGetMetricArgs\x1a\x14.SpanGetMetricReturn\"\x00\x12\x35\n\x0bSpanSetMeta\x12\x10.SpanSetMetaArgs\x1a\x12.SpanSetMetaReturn\"\x00\x12;\n\rSpanSetMetric\x12\x12.SpanSetMetricArgs\x1a\x14.SpanSetMetricReturn\"\x00\x12\x38\n\x0cSpanSetError\x12\x11.SpanSetErrorArgs\x1a\x13.SpanSetErrorReturn\"\x00\x12\x41\n\x0fSpanSetResource\x12\x14.SpanSetResourceArgs\x1a\x16.SpanSetResourceReturn\"\x00\x12\x35\n\x0bSpanAddLink\x12\x10.SpanAddLinkArgs\x1a\x12.SpanAddLinkReturn\"\x00\x12;\n\x11HTTPClientRequest\x12\x10.HTTPRequestArgs\x1a\x12.HTTPRequestReturn\"\x00\x12;\n\x11HTTPServerRequest\x12\x10.HTTPRequestArgs\x1a\x12.HTTPRequestReturn\"\x00\x12;\n\rInjectHeaders\x12\x12.InjectHeadersArgs\x1a\x14.InjectHeadersReturn\"\x00\x12\x32\n\nFlushSpans\x12\x0f.FlushSpansArgs\x1a\x11.FlushSpansReturn\"\x00\x12\x41\n\x0f\x46lushTraceStats\x12\x14.FlushTraceStatsArgs\x1a\x16.FlushTraceStatsReturn\"\x00\x12;\n\rOtelStartSpan\x12\x12.OtelStartSpanArgs\x1a\x14.OtelStartSpanReturn\"\x00\x12\x35\n\x0bOtelEndSpan\x12\x10.OtelEndSpanArgs\x1a\x12.OtelEndSpanReturn\"\x00\x12\x41\n\x0fOtelIsRecording\x12\x14.OtelIsRecordingArgs\x1a\x16.OtelIsRecordingReturn\"\x00\x12\x41\n\x0fOtelSpanContext\x12\x14.OtelSpanContextArgs\x1a\x16.OtelSpanContextReturn\"\x00\x12J\n\x12OtelSpanGetCurrent\x12\x17.OtelSpanGetCurrentArgs\x1a\x19.OtelSpanGetCurrentReturn\"\x00\x12;\n\rOtelSetStatus\x12\x12.OtelSetStatusArgs\x1a\x14.OtelSetStatusReturn\"\x00\x12\x35\n\x0bOtelSetName\x12\x10.OtelSetNameArgs\x1a\x12.OtelSetNameReturn\"\x00\x12G\n\x11OtelSetAttributes\x12\x16.OtelSetAttributesArgs\x1a\x18.OtelSetAttributesReturn\"\x00\x12>\n\x0eOtelFlushSpans\x12\x13.OtelFlushSpansArgs\x1a\x15.OtelFlushSpansReturn\"\x00\x12M\n\x13OtelFlushTraceStats\x12\x18.OtelFlushTraceStatsArgs\x1a\x1a.OtelFlushTraceStatsReturn\"\x00\x12\x44\n\x10OtelGetAttribute\x12\x15.OtelGetAttributeArgs\x1a\x17.OtelGetAttributeReturn\"\x00\x12\x35\n\x0bOtelGetName\x12\x10.OtelGetNameArgs\x1a\x12.OtelGetNameReturn\"\x00\x12\x38\n\x0cOtelGetLinks\x12\x11.OtelGetLinksArgs\x1a\x13.OtelGetLinksReturn\"\x00\x12\x32\n\nStopTracer\x12\x0f.StopTracerArgs\x1a\x11.StopTracerReturn\"\x00\x42&\n\x14\x63om.datadoghq.client\xaa\x02\rApmTestClientb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'protos.apm_test_client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\024com.datadoghq.client\252\002\rApmTestClient'
  _ATTRIBUTES_KEYVALSENTRY._options = None
  _ATTRIBUTES_KEYVALSENTRY._serialized_options = b'8\001'
  _STARTSPANARGS._serialized_start=33
  _STARTSPANARGS._serialized_end=363
  _DISTRIBUTEDHTTPHEADERS._serialized_start=365
  _DISTRIBUTEDHTTPHEADERS._serialized_end=425
  _SPANLINK._serialized_start=427
  _SPANLINK._serialized_end=548
  _HEADERTUPLE._serialized_start=550
  _HEADERTUPLE._serialized_end=591
  _STARTSPANRETURN._serialized_start=593
  _STARTSPANRETURN._serialized_end=645
  _INJECTHEADERSARGS._serialized_start=647
  _INJECTHEADERSARGS._serialized_end=683
  _INJECTHEADERSRETURN._serialized_start=685
  _INJECTHEADERSRETURN._serialized_end=775
  _FINISHSPANARGS._serialized_start=777
  _FINISHSPANARGS._serialized_end=805
  _FINISHSPANRETURN._serialized_start=807
  _FINISHSPANRETURN._serialized_end=825
  _SPANGETCURRENTARGS._serialized_start=827
  _SPANGETCURRENTARGS._serialized_end=847
  _SPANGETCURRENTRETURN._serialized_start=849
  _SPANGETCURRENTRETURN._serialized_end=906
  _SPANGETNAMEARGS._serialized_start=908
  _SPANGETNAMEARGS._serialized_end=942
  _SPANGETNAMERETURN._serialized_start=944
  _SPANGETNAMERETURN._serialized_end=977
  _SPANGETRESOURCEARGS._serialized_start=979
  _SPANGETRESOURCEARGS._serialized_end=1017
  _SPANGETRESOURCERETURN._serialized_start=1019
  _SPANGETRESOURCERETURN._serialized_end=1060
  _SPANGETMETAARGS._serialized_start=1062
  _SPANGETMETAARGS._serialized_end=1109
  _SPANGETMETARETURN._serialized_start=1111
  _SPANGETMETARETURN._serialized_end=1155
  _SPANGETMETRICARGS._serialized_start=1157
  _SPANGETMETRICARGS._serialized_end=1206
  _SPANGETMETRICRETURN._serialized_start=1208
  _SPANGETMETRICRETURN._serialized_end=1244
  _SPANSETMETAARGS._serialized_start=1246
  _SPANSETMETAARGS._serialized_end=1308
  _SPANSETMETARETURN._serialized_start=1310
  _SPANSETMETARETURN._serialized_end=1329
  _SPANSETMETRICARGS._serialized_start=1331
  _SPANSETMETRICARGS._serialized_end=1395
  _SPANSETMETRICRETURN._serialized_start=1397
  _SPANSETMETRICRETURN._serialized_end=1418
  _SPANSETERRORARGS._serialized_start=1420
  _SPANSETERRORARGS._serialized_end=1547
  _SPANSETERRORRETURN._serialized_start=1549
  _SPANSETERRORRETURN._serialized_end=1569
  _SPANSETRESOURCEARGS._serialized_start=1571
  _SPANSETRESOURCEARGS._serialized_end=1627
  _SPANSETRESOURCERETURN._serialized_start=1629
  _SPANSETRESOURCERETURN._serialized_end=1652
  _SPANADDLINKARGS._serialized_start=1654
  _SPANADDLINKARGS._serialized_end=1718
  _SPANADDLINKRETURN._serialized_start=1720
  _SPANADDLINKRETURN._serialized_end=1739
  _HTTPREQUESTARGS._serialized_start=1741
  _HTTPREQUESTARGS._serialized_end=1843
  _HTTPREQUESTRETURN._serialized_start=1845
  _HTTPREQUESTRETURN._serialized_end=1885
  _FLUSHSPANSARGS._serialized_start=1887
  _FLUSHSPANSARGS._serialized_end=1903
  _FLUSHSPANSRETURN._serialized_start=1905
  _FLUSHSPANSRETURN._serialized_end=1923
  _FLUSHTRACESTATSARGS._serialized_start=1925
  _FLUSHTRACESTATSARGS._serialized_end=1946
  _FLUSHTRACESTATSRETURN._serialized_start=1948
  _FLUSHTRACESTATSRETURN._serialized_end=1971
  _OTELSTARTSPANARGS._serialized_start=1974
  _OTELSTARTSPANARGS._serialized_end=2352
  _OTELSTARTSPANRETURN._serialized_start=2354
  _OTELSTARTSPANRETURN._serialized_end=2410
  _OTELENDSPANARGS._serialized_start=2412
  _OTELENDSPANARGS._serialized_end=2479
  _OTELENDSPANRETURN._serialized_start=2481
  _OTELENDSPANRETURN._serialized_end=2500
  _OTELFORCEFLUSHARGS._serialized_start=2502
  _OTELFORCEFLUSHARGS._serialized_end=2539
  _OTELFORCEFLUSHRETURN._serialized_start=2541
  _OTELFORCEFLUSHRETURN._serialized_end=2580
  _OTELFLUSHSPANSARGS._serialized_start=2582
  _OTELFLUSHSPANSARGS._serialized_end=2619
  _OTELFLUSHSPANSRETURN._serialized_start=2621
  _OTELFLUSHSPANSRETURN._serialized_end=2660
  _OTELFLUSHTRACESTATSARGS._serialized_start=2662
  _OTELFLUSHTRACESTATSARGS._serialized_end=2687
  _OTELFLUSHTRACESTATSRETURN._serialized_start=2689
  _OTELFLUSHTRACESTATSRETURN._serialized_end=2716
  _OTELSTOPTRACERARGS._serialized_start=2718
  _OTELSTOPTRACERARGS._serialized_end=2738
  _OTELSTOPTRACERRETURN._serialized_start=2740
  _OTELSTOPTRACERRETURN._serialized_end=2762
  _OTELISRECORDINGARGS._serialized_start=2764
  _OTELISRECORDINGARGS._serialized_end=2802
  _OTELISRECORDINGRETURN._serialized_start=2804
  _OTELISRECORDINGRETURN._serialized_end=2849
  _OTELSPANCONTEXTARGS._serialized_start=2851
  _OTELSPANCONTEXTARGS._serialized_end=2889
  _OTELSPANCONTEXTRETURN._serialized_start=2891
  _OTELSPANCONTEXTRETURN._serialized_end=3007
  _OTELSPANGETCURRENTARGS._serialized_start=3009
  _OTELSPANGETCURRENTARGS._serialized_end=3033
  _OTELSPANGETCURRENTRETURN._serialized_start=3035
  _OTELSPANGETCURRENTRETURN._serialized_end=3096
  _OTELSETSTATUSARGS._serialized_start=3098
  _OTELSETSTATUSARGS._serialized_end=3169
  _OTELSETSTATUSRETURN._serialized_start=3171
  _OTELSETSTATUSRETURN._serialized_end=3192
  _OTELSETNAMEARGS._serialized_start=3194
  _OTELSETNAMEARGS._serialized_end=3242
  _OTELSETNAMERETURN._serialized_start=3244
  _OTELSETNAMERETURN._serialized_end=3263
  _OTELSETATTRIBUTESARGS._serialized_start=3265
  _OTELSETATTRIBUTESARGS._serialized_end=3338
  _OTELSETATTRIBUTESRETURN._serialized_start=3340
  _OTELSETATTRIBUTESRETURN._serialized_end=3365
  _OTELGETATTRIBUTEARGS._serialized_start=3367
  _OTELGETATTRIBUTEARGS._serialized_end=3419
  _OTELGETATTRIBUTERETURN._serialized_start=3421
  _OTELGETATTRIBUTERETURN._serialized_end=3470
  _OTELGETNAMEARGS._serialized_start=3472
  _OTELGETNAMEARGS._serialized_end=3506
  _OTELGETNAMERETURN._serialized_start=3508
  _OTELGETNAMERETURN._serialized_end=3541
  _OTELGETLINKSARGS._serialized_start=3543
  _OTELGETLINKSARGS._serialized_end=3578
  _OTELGETLINKSRETURN._serialized_start=3580
  _OTELGETLINKSRETURN._serialized_end=3626
  _ATTRIBUTES._serialized_start=3628
  _ATTRIBUTES._serialized_end=3742
  _ATTRIBUTES_KEYVALSENTRY._serialized_start=3686
  _ATTRIBUTES_KEYVALSENTRY._serialized_end=3742
  _LISTVAL._serialized_start=3744
  _LISTVAL._serialized_end=3776
  _ATTRVAL._serialized_start=3778
  _ATTRVAL._serialized_end=3881
  _STOPTRACERARGS._serialized_start=3883
  _STOPTRACERARGS._serialized_end=3899
  _STOPTRACERRETURN._serialized_start=3901
  _STOPTRACERRETURN._serialized_end=3919
  _APMCLIENT._serialized_start=3922
  _APMCLIENT._serialized_end=5827
# @@protoc_insertion_point(module_scope)
