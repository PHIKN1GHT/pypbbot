from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    pass

from typing import Union
from pypbbot.protocol import onebot_api_pb2, onebot_event_pb2, onebot_frame_pb2, onebot_base_pb2
from pypbbot.protocol import *

ProtobufBotAPI = Union[onebot_api_pb2.SendPrivateMsgReq, onebot_api_pb2.SendPrivateMsgResp, onebot_api_pb2.SendGroupMsgReq, onebot_api_pb2.SendGroupMsgResp, onebot_api_pb2.SendMsgReq, onebot_api_pb2.SendMsgResp, onebot_api_pb2.DeleteMsgReq, onebot_api_pb2.DeleteMsgResp, onebot_api_pb2.GetMsgReq, onebot_api_pb2.GetMsgResp, onebot_api_pb2.GetForwardMsgReq, onebot_api_pb2.GetForwardMsgResp, onebot_api_pb2.SendLikeReq, onebot_api_pb2.SendLikeResp, onebot_api_pb2.SetGroupKickReq, onebot_api_pb2.SetGroupKickResp, onebot_api_pb2.SetGroupBanReq, onebot_api_pb2.SetGroupBanResp, onebot_api_pb2.SetGroupAnonymousBanReq, onebot_api_pb2.SetGroupAnonymousBanResp, onebot_api_pb2.SetGroupWholeBanReq, onebot_api_pb2.SetGroupWholeBanResp, onebot_api_pb2.SetGroupAdminReq, onebot_api_pb2.SetGroupAdminResp, onebot_api_pb2.SetGroupAnonymousReq, onebot_api_pb2.SetGroupAnonymousResp, onebot_api_pb2.SetGroupCardReq, onebot_api_pb2.SetGroupCardResp, onebot_api_pb2.SetGroupNameReq, onebot_api_pb2.SetGroupNameResp, onebot_api_pb2.SetGroupLeaveReq, onebot_api_pb2.SetGroupLeaveResp, onebot_api_pb2.SetGroupSpecialTitleReq, onebot_api_pb2.SetGroupSpecialTitleResp, onebot_api_pb2.SetFriendAddRequestReq, onebot_api_pb2.SetFriendAddRequestResp, onebot_api_pb2.SetGroupAddRequestReq,
                       onebot_api_pb2.SetGroupAddRequestResp, onebot_api_pb2.GetLoginInfoReq, onebot_api_pb2.GetLoginInfoResp, onebot_api_pb2.GetStrangerInfoReq, onebot_api_pb2.GetStrangerInfoResp, onebot_api_pb2.GetFriendListReq, onebot_api_pb2.GetFriendListResp, onebot_api_pb2.GetGroupInfoReq, onebot_api_pb2.GetGroupInfoResp, onebot_api_pb2.GetGroupListReq, onebot_api_pb2.GetGroupListResp, onebot_api_pb2.GetGroupMemberInfoReq, onebot_api_pb2.GetGroupMemberInfoResp, onebot_api_pb2.GetGroupMemberListReq, onebot_api_pb2.GetGroupMemberListResp, onebot_api_pb2.GetGroupHonorInfoReq, onebot_api_pb2.GetGroupHonorInfoResp, onebot_api_pb2.GetCookiesReq, onebot_api_pb2.GetCookiesResp, onebot_api_pb2.GetCsrfTokenReq, onebot_api_pb2.GetCsrfTokenResp, onebot_api_pb2.GetCredentialsReq, onebot_api_pb2.GetCredentialsResp, onebot_api_pb2.GetRecordReq, onebot_api_pb2.GetRecordResp, onebot_api_pb2.GetImageReq, onebot_api_pb2.GetImageResp, onebot_api_pb2.CanSendImageReq, onebot_api_pb2.CanSendImageResp, onebot_api_pb2.CanSendRecordReq, onebot_api_pb2.CanSendRecordResp, onebot_api_pb2.GetStatusReq, onebot_api_pb2.GetStatusResp, onebot_api_pb2.GetVersionInfoReq, onebot_api_pb2.GetVersionInfoResp, onebot_api_pb2.SetRestartReq, onebot_api_pb2.SetRestartResp, onebot_api_pb2.CleanCacheReq, onebot_api_pb2.CleanCacheResp]
''' Genrated by: 
    ProtobufBotAPI = Union[tuple([getattr(onebot_api_pb2, attr) for attr in onebot_api_pb2.__dir__() if attr.endswith('Req') or attr.endswith('Resp')])]
'''

ProtobufBotEvent = Union[onebot_event_pb2.PrivateMessageEvent, onebot_event_pb2.GroupMessageEvent, onebot_event_pb2.GroupUploadNoticeEvent, onebot_event_pb2.GroupAdminNoticeEvent, onebot_event_pb2.GroupDecreaseNoticeEvent, onebot_event_pb2.GroupIncreaseNoticeEvent,
                         onebot_event_pb2.GroupBanNoticeEvent, onebot_event_pb2.FriendAddNoticeEvent, onebot_event_pb2.GroupRecallNoticeEvent, onebot_event_pb2.FriendRecallNoticeEvent, onebot_event_pb2.FriendRequestEvent, onebot_event_pb2.GroupRequestEvent]
''' Genrated by: 
    ProtobufBotEvent = Union[tuple([getattr(onebot_event_pb2, attr) for attr in onebot_event_pb2.__dir__() if attr.endswith('Event')])]
'''

ProtobufBotFrame = onebot_frame_pb2.Frame
ProtobufBotMessage = onebot_base_pb2.Message
ProtobufBotMessageEvent = Union[onebot_event_pb2.PrivateMessageEvent,
                                onebot_event_pb2.GroupMessageEvent]


Event = Union[ProtobufBotEvent]
