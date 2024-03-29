from datetime import datetime
from unittest import TestCase

from src.application.use_cases.post_message_use_case import PostMessageCommand
from src.tests.builders.message_builder import MessageBuilder
from src.domain.message_text_exceptions import (
    MessageTextTooLongError,
    MessageTextEmptyError,
)
from src.tests.fixtures.message_fixture import MessageFixture


class TestPostingMessage(TestCase):
    def setUp(self) -> None:
        self.message_fixture = MessageFixture()

    """
    Rule: a message must have a max length of 280 characters
    """

    def test_user_can_post_a_message_on_his_timeline(self):
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.message_fixture.when_user_posts_a_message(
            PostMessageCommand(id="message-id", text="Hello everyone", author="Bob")
        )
        self.message_fixture.then_posted_message_should_be(
            MessageBuilder()
            .written_by("Bob")
            .with_id("message-id")
            .with_text("Hello everyone")
            .on("2022-06-04T19:00:00")
            .build(),
        )

    def test_user_cannot_post_a_message_on_his_timeline_with_more_than_280_characters(
        self,
    ):
        text_with_more_than_280_characters = (
            "Lorem ipsum dolor sit amet, consectetur "
            "adipiscing elit. Cras mauris lacus, fringilla eu est vitae, varius "
            "viverra nisl. Pellentesque habitant morbi tristique senectus et netus "
            "et malesuada fames ac turpis egestas. Vivamus suscipit feugiat "
            "sollicitudin. Aliquam erat volutpat amet."
        )
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.message_fixture.when_user_posts_a_message(
            PostMessageCommand(
                id="message-id", text=text_with_more_than_280_characters, author="Bob"
            )
        )
        self.message_fixture.then_posting_should_be_refused_with_error(
            MessageTextTooLongError
        )

    """
    Rule: a message cannot be empty
    """

    def test_user_cannot_post_an_empty_message_on_his_timeline(self):
        text_empty = ""
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.message_fixture.when_user_posts_a_message(
            PostMessageCommand(id="message-id", text=text_empty, author="Bob")
        )
        self.message_fixture.then_posting_should_be_refused_with_error(
            MessageTextEmptyError
        )

    def test_user_cannot_post_a_message_on_his_timeline_with_only_space_characters(
        self,
    ):
        text_with_only_space_characters = "      "
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=0, second=0)
        )
        self.message_fixture.when_user_posts_a_message(
            PostMessageCommand(
                id="message-id", text=text_with_only_space_characters, author="Bob"
            )
        )
        self.message_fixture.then_posting_should_be_refused_with_error(
            MessageTextEmptyError
        )
