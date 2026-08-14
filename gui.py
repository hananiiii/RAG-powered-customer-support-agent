import streamlit as st

class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        self.messages = assistant.messages

    def get_response(self, user_input):
        return self.assistant.get_response(user_input)

    def render_messages(self):
        messages = self.messages
        for message in messages:
            if message["role"] == "user":
                st.chat_message("human").markdown(message["content"])
            if message["role"] == "ai":
                st.chat_message("ai").markdown(message["content"])

    def set_state(self, key, value):
        st.session_state[key] = value

    def render_sources(self):
        # NEW: displays the retrieved chunks in a collapsible expander
        sources = self.assistant.last_sources
        if sources:
            with st.expander("📄 Sources used for this answer"):
                for i, doc in enumerate(sources, 1):
                    page = doc.metadata.get("page", "unknown")
                    st.markdown(f"**Source {i}** (page {page})")
                    st.caption(doc.page_content[:300] + "...")

    def render_user_input(self):
        user_input = st.chat_input("Ask us anything...", key="input")
        if user_input and user_input != "":
            st.chat_message("human").markdown(user_input)

            response_generator = self.get_response(user_input)

            with st.chat_message("ai"):
                response = st.write_stream(response_generator)
                self.render_sources()  # NEW: show sources right after the answer

            self.messages.append({"role": "user", "content": user_input})
            self.messages.append({"role": "ai", "content": response})

            self.set_state("messages", self.messages)

    def render_clear_button(self):
        # NEW: clear chat button in the sidebar
        if st.button("🗑️ Clear Conversation"):
            welcome = self.messages[0]  # keep the original welcome message
            self.messages.clear()
            self.messages.append(welcome)
            self.set_state("messages", self.messages)
            st.rerun()

    def render(self):
        with st.sidebar:
            st.title("💬 Customer Support")
            st.write("Ask us about orders, shipping, returns, and more!")
            st.divider()
            self.render_clear_button()  # NEW

        self.render_messages()
        self.render_user_input()