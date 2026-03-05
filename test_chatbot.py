# test_chatbot.py
"""Automated tests for the chatbot application."""

import pytest

# Import the Flask app and helper functions
from app import app, check_for_crisis


class TestCrisisDetection:
    """Tests for the crisis keyword detection feature."""

    def test_crisis_keyword_detected(self):
        """TC-004: Crisis keywords should be detected."""
        # Test various crisis phrases
        assert check_for_crisis("I don't want to live anymore") == True
        assert check_for_crisis("thinking about suicide") == True
        assert check_for_crisis("want to die") == True

    def test_normal_message_not_flagged(self):
        """Normal messages should NOT trigger crisis detection."""
        assert check_for_crisis("Hello, how are you?") == False
        assert check_for_crisis("What's the weather like?") == False
        assert check_for_crisis("Tell me a joke") == False

    def test_case_insensitive(self):
        """Crisis detection should work regardless of case."""
        assert check_for_crisis("SUICIDE") == True
        assert check_for_crisis("SuIcIdE") == True


@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat messages and return bot responses."""
    data = request.get_json()
    raw_message = data.get("message", "")

    # Sanitise and validate input
    user_message = sanitise_input(raw_message)

    if user_message is None:
        if not raw_message or not raw_message.strip():
            return jsonify({"response": "Please enter a message!"})
        else:
            return jsonify(
                {"response": "Message too long! Please keep it under 500 characters."}
            )

    # Safety check for crisis keywords (use original for better detection)
    if check_for_crisis(raw_message):
        return jsonify({"response": CRISIS_RESPONSE})

    # Get the chatbot's response
    bot_response = chatbot.get_response(user_message)

    return jsonify({"response": str(bot_response)})
    return jsonify({"response": str(bot_response)})


from app import sanitise_input


class TestInputSanitisation:
    """Tests for input sanitisation."""

    def test_strips_whitespace(self):
        """Leading and trailing whitespace should be removed."""
        assert sanitise_input("  hello  ") == "hello"

    def test_rejects_whitespace_only(self):
        """Messages with only whitespace should be rejected."""
        assert sanitise_input("     ") is None
        assert sanitise_input("\n\t\n") is None

    def test_strips_html_tags(self):
        """HTML tags should be removed."""
        assert sanitise_input("<b>hello</b>") == "hello"
        assert sanitise_input("<script>alert('x')</script>") == "alert('x')"

    def test_rejects_too_long(self):
        """Messages over 500 chars should be rejected."""
        assert sanitise_input("a" * 501) is None
        assert sanitise_input("a" * 500) == "a" * 500
