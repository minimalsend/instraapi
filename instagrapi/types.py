from typing import List, Optional
from .validators import BaseModel, HttpUrl, FilePath, Datetime


class Resource(BaseModel):
    pk: int
    video_url: Optional[HttpUrl] = None  # for Video and IGTV
    thumbnail_url: Optional[HttpUrl] = None
    media_type: int


class User(BaseModel):
    pk: int
    username: str
    full_name: str
    is_private: bool
    profile_pic_url: Optional[HttpUrl] = None
    is_verified: bool
    media_count: int
    follower_count: int
    following_count: int
    biography: Optional[str] = ''
    external_url: Optional[HttpUrl] = None
    is_business: bool


class Account(User):
    birthday: Optional[str] = None
    phone_number: Optional[str] = None
    gender: Optional[int] = None
    email: Optional[str] = None


class UserShort(BaseModel):
    pk: int
    username: Optional[str] = None
    full_name: Optional[str] = ''
    profile_pic_url: Optional[HttpUrl] = None


class Usertag(BaseModel):
    user: UserShort
    x: Optional[float] = None
    y: Optional[float] = None


class Location(BaseModel):
    pk: Optional[int] = None
    name: str
    address: Optional[str] = ''
    lng: Optional[float] = None
    lat: Optional[float] = None
    external_id: Optional[int] = None
    external_id_source: Optional[str] = None


class ClipsMetadata(BaseModel):
    original_sound_info: Optional[dict] = None  # <-- Corrigido para aceitar None


class Media(BaseModel):
    pk: int
    id: str
    code: str
    taken_at: Datetime
    media_type: int
    product_type: Optional[str] = ''  # only for IGTV
    thumbnail_url: Optional[HttpUrl] = None
    location: Optional[Location] = None
    user: UserShort
    comment_count: int
    like_count: int
    has_liked: Optional[bool] = None
    caption_text: str = ''
    usertags: Optional[List[Usertag]] = []
    video_url: Optional[HttpUrl] = None  # for Video and IGTV
    view_count: Optional[int] = 0  # for Video and IGTV
    video_duration: Optional[float] = 0.0  # for Video and IGTV
    title: Optional[str] = ''
    resources: Optional[List[Resource]] = []
    clips_metadata: Optional[ClipsMetadata] = None  # <-- Corrigido para aceitar None


class DirectMessage(BaseModel):
    id: int
    user_id: Optional[int] = None
    thread_id: Optional[int] = None
    timestamp: Datetime
    item_type: Optional[str] = None
    is_shh_mode: Optional[bool] = None
    reactions: Optional[dict] = None
    text: Optional[str] = None
    media_share: Optional[Media] = None
    reel_share: Optional[Media] = None
    story_share: Optional[dict] = None
    felix_share: Optional[dict] = None
    placeholder: Optional[dict] = None


class DirectThread(BaseModel):
    pk: int
    id: int
    messages: Optional[List[DirectMessage]] = []
    users: Optional[List[UserShort]] = []
    inviter: Optional[UserShort] = None
    left_users: Optional[List[UserShort]] = []
    admin_user_ids: Optional[List[int]] = []
    last_activity_at: Datetime
    muted: bool
    is_pin: bool
    named: bool
    canonical: bool
    pending: bool
    archived: bool
    thread_type: str
    thread_title: str
    folder: int
    vc_muted: bool
    is_group: bool
    mentions_muted: bool
    approval_required_for_new_members: bool
    input_mode: int
    business_thread_folder: int
    read_state: int
    is_close_friend_thread: bool
    assigned_admin_id: int
    shh_mode_enabled: bool
    last_seen_at: Optional[dict] = {}

    def is_seen(self, user_id: int):
        user_id = str(user_id)
        own_timestamp = int(self.last_seen_at.get(user_id, {}).get('timestamp', 0))
        timestamps = [
            (int(v.get('timestamp', 0)) - own_timestamp) > 0
            for k, v in self.last_seen_at.items()
            if k != user_id
        ]
        return not any(timestamps)
