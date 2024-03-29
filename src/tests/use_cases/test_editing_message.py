from datetime import datetime
from unittest import TestCase

from src.tests.builders.message_builder import MessageBuilder
from src.application.use_cases.edit_message_use_case import EditMessageCommand
from src.domain.message_text_exceptions import (
    MessageTextTooLongError,
    MessageTextEmptyError,
)
from src.tests.fixtures.message_fixture import MessageFixture


class TestEditingMessage(TestCase):
    original_message = (
        MessageBuilder()
        .written_by("Bob")
        .with_id("message-id-4")
        .with_text("Bob's last message")
        .on("2022-06-04T19:02:20")
        .build()
    )

    def setUp(self) -> None:
        self.message_fixture = MessageFixture()

    """
    Rule: a message must have a max length of 280 characters
    """

    def test_user_can_edit_a_message_on_his_timeline(self):
        self.message_fixture.given_following_messages_exist([self.original_message])
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.message_fixture.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text="Bob's edited message",
            )
        )
        self.message_fixture.then_edited_message_should_be(
            MessageBuilder()
            .written_by("Bob")
            .with_id("message-id-4")
            .with_text("Bob's edited message")
            .on("2022-06-04T19:10:00")
            .build(),
        )

    def test_user_cannot_edit_a_message_on_his_timeline_to_more_than_280_characters(
        self,
    ):
        text_with_more_than_280_characters = (
            "Lorem ipsum dolor sit amet, consectetur "
            "adipiscing elit. Cras mauris lacus, fringilla eu est vitae, varius "
            "viverra nisl. Pellentesque habitant morbi tristique senectus et netus "
            "et malesuada fames ac turpis egestas. Vivamus suscipit feugiat "
            "sollicitudin. Aliquam erat volutpat amet."
        )
        self.message_fixture.given_following_messages_exist([self.original_message])
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.message_fixture.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text=text_with_more_than_280_characters,
            )
        )
        self.message_fixture.then_editing_should_be_refused_with_error(
            expected_error=MessageTextTooLongError
        )
        self.message_fixture.then_message_should_be(self.original_message)

    """
    Rule: a message cannot be empty
    """

    def test_user_cannot_edit_a_message_on_his_timeline_to_an_empty_message(self):
        text_empty = ""
        self.message_fixture.given_following_messages_exist([self.original_message])
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.message_fixture.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text=text_empty,
            )
        )
        self.message_fixture.then_editing_should_be_refused_with_error(
            expected_error=MessageTextEmptyError
        )
        self.message_fixture.then_message_should_be(self.original_message)

    def test_user_cannot_edit_a_message_on_his_timeline_to_only_space_characters(
        self,
    ):
        text_with_only_space_characters = "      "
        self.message_fixture.given_following_messages_exist([self.original_message])
        self.message_fixture.given_now_is(
            datetime(year=2022, month=6, day=4, hour=19, minute=10, second=0)
        )
        self.message_fixture.when_user_edits_message(
            EditMessageCommand(
                author="Bob",
                id="message-id-4",
                text=text_with_only_space_characters,
            )
        )
        self.message_fixture.then_editing_should_be_refused_with_error(
            expected_error=MessageTextEmptyError
        )
        self.message_fixture.then_message_should_be(self.original_message)
