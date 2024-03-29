from datetime import datetime
from typing import List

from src.infrastructure.adapters.in_memory_message_repository import (
    InMemoryMessageRepository,
)
from src.domain.message import Message
from src.application.use_cases.post_message_use_case import (
    PostMessageCommand,
    PostMessageUseCase,
)
from src.application.use_cases.edit_message_use_case import (
    EditMessageUseCase,
    EditMessageCommand,
)
from src.domain.message_text_exceptions import (
    MessageTextTooLongError,
    MessageTextEmptyError,
)
from src.application.use_cases.view_timeline_use_case import ViewTimelineUseCase
from src.infrastructure.adapters.stub_date_time_provider import StubDateTimeProvider


class MessageFixture:
    def __init__(self):
        self.thrown_error = None
        self.message_repository = InMemoryMessageRepository()
        self.date_time_provider = StubDateTimeProvider()
        self.displayed_timeline = None

    # GIVEN
    # =====
    def given_now_is(self, date_time: datetime):
        self.date_time_provider.now = date_time

    def given_following_messages_exist(self, messages: List[Message]):
        self.message_repository.given_existing_messages(messages)

    # WHEN
    # ====
    def when_user_posts_a_message(self, message_command: PostMessageCommand):
        try:
            postMessageUseCase = PostMessageUseCase(
                self.message_repository, self.date_time_provider
            )
            postMessageUseCase.handle(message_command)
        except Exception as e:
            self.thrown_error = e

    def when_user_wants_to_view_his_timeline(self, author: str):
        view_timeline_use_case = ViewTimelineUseCase(
            self.message_repository, self.date_time_provider
        )
        self.displayed_timeline = view_timeline_use_case.handle(author)

    def when_user_edits_message(self, message_command: EditMessageCommand):
        try:
            edit_message_use_case = EditMessageUseCase(
                self.message_repository, self.date_time_provider
            )
            self.edited_message = edit_message_use_case.handle(message_command)
        except Exception as e:
            self.thrown_error = e

    # THEN
    # ====
    def then_displayed_timeline_should_be(self, expected_timeline: List[dict]):
        assert self.displayed_timeline == expected_timeline

    def then_posted_message_should_be(self, expected_message: Message):
        self.then_message_should_be(expected_message)

    def then_posting_should_be_refused_with_error(
        self, expected_error: [MessageTextTooLongError, MessageTextEmptyError]
    ):
        assert isinstance(self.thrown_error, expected_error)

    def then_edited_message_should_be(self, expected_message: Message):
        return self.then_message_should_be(expected_message)

    def then_editing_should_be_refused_with_error(
        self, expected_error: [MessageTextTooLongError]
    ):
        assert isinstance(self.thrown_error, expected_error)

    def then_message_should_be(self, expected_message: Message):
        assert (
            self.message_repository.get_by_id(expected_message.id) == expected_message
        )
