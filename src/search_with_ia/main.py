import gradio as gr
import html
from agents_swarm import AgentsSwarm

class SearchWithAIApp:
    def __init__(self):
        with gr.Blocks(title="Search with AI", fill_width=True) as app:
            with gr.Column():
                gr.Markdown("# Search with AI")

                chatbot = gr.Chatbot(height="70vh", type="messages")

                with gr.Row():
                    user_input_textbox = gr.Textbox(show_label=False, placeholder="Ask your question")

                user_input_textbox.submit(fn=self.on_user_input_entered, inputs=[user_input_textbox, chatbot], outputs=[user_input_textbox, chatbot])

        self.app = app

    def on_user_input_entered(self, user_input: gr.Textbox, chat_history: gr.Chatbot) -> list[str, gr.Chatbot]:
        agents_swarm = AgentsSwarm()
        response = agents_swarm.execute(user_input)

        chat_history.append({"role": "user", "content": html.escape(user_input)})
        chat_history.append({"role": "assistant", "content": html.escape(response)})

        return ["", chat_history]

    def launch(self):
        self.app.launch()

if __name__ == "__main__":
    chat_app = SearchWithAIApp()
    chat_app.launch()