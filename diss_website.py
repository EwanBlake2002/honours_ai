"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx  # Reflex framework for building web apps
import random  # For generating random values
from rxconfig import config  # Configuration for Reflex app
from reflex.style import set_color_mode, color_mode  # For handling color modes (light/dark)
import smtplib  # For sending emails
from email.mime.text import MIMEText  # For creating email content
from email.mime.multipart import MIMEMultipart  # For creating multipart emails
import copy  # For deep copying objects
import time  # For time-related operations
from typing import Any, List, Union  # For type hints
import os  # For interacting with the operating system


# Component for a top banner that can be toggled on/off
class TopBannerBasic(rx.ComponentState):
    hide: bool = False  # State to track if the banner is hidden

    # Event handler to toggle the banner visibility
    @rx.event
    def toggle(self):
        self.hide = not self.hide

    # Method to render the banner component
    @classmethod
    def get_component(cls, **props):
        return rx.cond(
            ~cls.hide,  # Show the banner if not hidden
            rx.hstack(
                rx.flex(
                    rx.badge(
                        rx.icon("circle-help", size=18, aria_label="Help icon"),
                        padding="0.30rem",
                        radius="full",
                        color="#333333",
                    ),
                    rx.text(
                        "Want To Try Our AI Quiz? - ",
                        rx.link(
                            "Try AI Quiz!",
                            href="/resources/user-experiences#quiz-form",
                            underline="always",
                            display="inline",
                            underline_offset="2px",
                            color="#333333",
                            aria_label="Link to AI Quiz form section",
                        ),
                        weight="medium",
                        font_family="Montserrat",
                        color="#333333",
                    ),
                    align="center",
                    margin="auto",
                    spacing="3",
                    role="alert",  # Accessibility: mark banner as an alert
                ),
                rx.icon(
                    "x",
                    cursor="pointer",
                    justify="end",
                    flex_shrink=0,
                    on_click=cls.toggle,  # Toggle banner on click
                    color="#ffffff",
                    aria_label="Dismiss banner",  # Accessibility label
                    role="button",
                    tab_index="0",  # Make it keyboard focusable
                ),
                wrap="nowrap",
                justify="between",
                width="100%",
                align="center",
                left="0",
                padding="1rem",
                background_color="rgba(255, 127, 80)",  # Coral background color
                **props,
            ),
            # Fallback: Show a button to toggle the banner back on
            rx.icon_button(
                rx.icon("eye", aria_label="Show banner"),
                cursor="pointer",
                on_click=cls.toggle,
                aria_label="Show banner toggle button",
            ),
        )



# Base styling for components
base_style = {
    "background_color": "white",  # White background
    "color": "black",  # Black text
    "padding": "20px",
    "border_radius": "10px",
    "box_shadow": "0 4px 8px rgba(0, 0, 0, 0.2)",  # Shadow effect
    "width": "100%",  # Full width
    "max_width": "600px",  # Maximum width
}

# Style for questions
question_style = base_style | {"width": "100%"}

# Background color for the page
page_background = rx.color("gray", 3)


SMTP_SERVER = "smtp.gmail.com"  
SMTP_PORT = 587  
EMAIL_ADDRESS = "ewanblake02@gmail.com" 
EMAIL_PASSWORD = "mcnh mvod zkvo ejru"  


# State for the contact form
class ContactFormState(rx.State):
    name: str = ""  # User's name
    email: str = ""  # User's email
    contact: str = ""  # Priority level
    subject: str = ""  # Suggested change or addition
    issue: str = ""  # Details of the suggestion
    status: str = ""  # Submission status message

    # Handle form submission
    def handle_submit(self):
        # Create email content
        email_content = f"""
        Name: {self.name}
        Email: {self.email}
        Suggested Change or Addition: {self.subject}
        Priority Level: {self.contact}
        Details of Suggestion: {self.issue}
        """

        # Create the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS  # Send the email to yourself
        msg["Subject"] = f"New Website Suggestion: {self.subject}"
        msg.attach(MIMEText(email_content, "plain"))

        try:
            # Connect to the SMTP server and send the email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()  # Upgrade to secure connection
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)  # Log in to the server
                server.send_message(msg)  # Send the email
            self.status = "Suggestion submitted successfully!"
        except Exception as e:
            self.status = f"Failed to submit suggestion: {str(e)}"


def dark_mode_toggle() -> rx.Component:
    return rx.segmented_control.root(
        rx.segmented_control.item(
            rx.icon(tag="monitor", size=20, aria_label="System Default Mode"),
            value="system",
            aria_label="System Default Mode",
        ),
        rx.segmented_control.item(
            rx.icon(tag="sun", size=20, aria_label="Light Mode"),
            value="light",
            aria_label="Light Mode",
        ),
        rx.segmented_control.item(
            rx.icon(tag="moon", size=20, aria_label="Dark Mode"),
            value="dark",
            aria_label="Dark Mode",
        ),
        on_change=State.set_color_mode,
        variant="classic",
        radius="large",
        value=State.color_mode,
        role="radiogroup",
        aria_label="Toggle color mode",
    )



def breadcrumb_trail(crumbs: list[tuple[str, str]]) -> rx.Component:
    """
    Generates a breadcrumb trail with hover effect for links.
    :param crumbs: A list of tuples containing (label, href).
                   Example: [("Home", "/"), ("Resources", "/resources"), ("Current Page", "")]
    """
    items = []

    # Custom hover effect style
    hover_effect_style = {
        "display": "inline-block",
        "position": "relative",
        "overflow": "hidden",
        "color": "#270042",  #
        "transition": "color 0.3s ease",
        "text-decoration": "none",
        "font-family": "Poppins",
        "font-size": "16px",  
        "@media (max-width: 768px)": {
            "font-size": "14px",
            "margin-right": "12px",
        },
        "&:before": {
            "content": '""',
            "position": "absolute",
            "left": "0",
            "bottom": "0",
            "width": "100%",
            "height": "2px",
            "background": "purple",
            "transform": "translateX(-100%)",
            "transition": "transform 0.3s ease",
        },
        "&:hover": {
            "color": "#270042",
        },
        "&:hover:before": {
            "transform": "translateX(0)",
        },
    }

    # Generate breadcrumb items
    for index, (label, href) in enumerate(crumbs):
        if href:
            items.append(
                rx.link(
                    label,
                    href=href,
                    style=hover_effect_style,
                    aria_label=f"Navigate to {label}",  # Screen reader label
                )
            )
        else:
            items.append(
                rx.text(
                    label,
                    color="gray",
                    aria_current="page",  # Accessibility: mark as current page
                )
            )

        if index < len(crumbs) - 1:
            items.append(rx.text("→", color="black", font_weight="bold", role="presentation"))  # Decorative

    return rx.hstack(
        *items,
        padding="0.5em 2em",
        bg="#FF7F50",
        margin_top="-12px",
        border_bottom_right_radius="20px",
        flex_wrap="wrap",
        gap="10px",
        role="navigation",  # Identifies this section as navigation
        aria_label="Breadcrumb",  # Screen reader context
        style={"@media (max-width: 768px)": {"gap": "15px", "padding": "0.5em"}},
    )



def navbar_link(label: str, href: str):
    return rx.link(
        rx.text(
            label,
            size="4",
            weight="medium",
            color="white",
            font_family="Poppins",
        ),
        href=href,
        aria_label=f"Navigate to {label}",  # Descriptive for screen readers
        _hover={"text_decoration": "none", "color": "#F3F4F6"},
    )



# Main app state
class State(rx.State):
    """The app state."""

    default_answers = [None, None, None, None, None]  # Initialize with None for 5 questions
    answers: List[Any] = default_answers  # User's answers
    answer_key = [
        "Neurons",  # Correct answer for Question 1
        "To evaluate the difference between predicted and actual values",  # Correct answer for Question 2
        "All of the above",  # Correct answer for Question 3
        "To learn a policy that maximizes cumulative rewards",  # Correct answer for Question 4
        "Both 1 and 3",  # Correct answer for Question 5
    ]
    score: int = 0  # User's score

    # Reset answers when the page loads
    def onload(self):
        self.answers = copy.deepcopy(self.default_answers)

    # Update user's answers
    def set_answers(self, answer, index, sub_index=None):
        if sub_index is None:
            self.answers[index] = answer
        else:
            self.answers[index][sub_index] = answer

    # Calculate score and redirect to results page
    def submit(self):
        total, correct = 0, 0
        for i in range(len(self.answers)):
            if self.answers[i] == self.answer_key[i]:
                correct += 1
            total += 1

        # Avoid division by zero
        if total == 0:
            self.score = 0
        else:
            self.score = int(correct / total * 100)

        return rx.redirect("//resources/educational-resources/result")

    # Return score as a percentage string
    @rx.var
    def percent_score(self) -> str:
        return f"{self.score}%"

    color_mode: str = "light"  # Default to light mode

    # Update color mode
    def set_color_mode(self, color_mode: Union[str, List[str]]):
        if isinstance(color_mode, list):
            self.color_mode = color_mode[0]  # Use the first value
        else:
            self.color_mode = color_mode


def header():
    return rx.vstack(
        rx.heading(
            "AI Quiz", 
            color="black", 
            id="quiz-heading",
            style={
                "font-size": "24px",
                "@media (max-width: 768px)": {"font-size": "20px"}
            }
        ),
        rx.divider(**{"aria-hidden": "true"}),
        rx.text(
            "Test your knowledge of Artificial Intelligence (AI) concepts!",
            color="black",
            style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
            **{"aria-describedby": "quiz-heading"}  
        ),
        rx.text(
            "Once submitted, your results will be shown on the results page.",
            color="black",
            style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}}
        ),
        style=question_style,
    )




def question1():
    return rx.vstack(
        rx.heading(
            "Question #1",
            color="black",
            style={"font-size": "20px", "@media (max-width: 768px)": {"font-size": "18px"}},
            id="question1-heading"
        ),
        rx.text(
            "Which of the following is a key component of a neural network?",
            color="black",
            as_="label",
            html_for="question1-radio-group",
            id="question1-label",
            style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
        ),
        rx.divider(**{"aria-hidden": "true"}),
        rx.box(
            rx.text(
                "Select the correct answer:",
                color="black",
                id="question1-desc",
                style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
            ),
            rx.radio_group(
                items=["Neurons", "Decision Trees", "Support Vector Machines", "K-Means Clustering"],
                default_value=State.answers[0],
                on_change=lambda answer: State.set_answers(answer, 0),
                color="black",
                id="question1-radio-group",
                **{
                    "aria-labelledby": "question1-label question1-desc",
                },
            ),
        ),
    )



def question2():
    return rx.vstack(
        rx.heading(
            "Question #2",
            color="black",
            style={"font-size": "20px", "@media (max-width: 768px)": {"font-size": "18px"}},
            id="question2-heading"
        ),
        rx.text(
            "What is the primary purpose of a loss function in machine learning?",
            color="black",
            as_="label",  
            html_for="question2-radio-group",  # Added association with radio group
            id="question2-label",
            style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
        ),
        rx.divider(**{"aria-hidden": "true"}),
        rx.box(
            rx.text(
                "Select the correct answer:",
                color="black",
                id="question2-desc",
                style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
            ),
            rx.radio_group(
                items=[
                    "To measure the accuracy of the model",
                    "To optimize the model's parameters", 
                    "To evaluate the difference between predicted and actual values",
                    "To visualize the data",
                ],
                default_value=State.answers[1],
                on_change=lambda answer: State.set_answers(answer, 1),
                color="black",
                id="question2-radio-group",  # Added ID to match html_for
                **{
                    "aria-labelledby": "question2-label question2-desc",  # Combined both references
                },
            ),
        ),
    )



def question3():
    return rx.vstack(
        rx.heading(
            "Question #3",
            color="black",
            style={"font-size": "20px", "@media (max-width: 768px)": {"font-size": "18px"}},
            id="question3-heading"
        ),
        rx.text(
            "Which of the following is a valid activation function used in neural networks?",
            color="black",
            as_="label",
            html_for="question3-radio-group",
            id="question3-label",
            style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
        ),
        rx.divider(**{"aria-hidden": "true"}),
        rx.box(
            rx.text(
                "Select the correct answer:",
                color="black",
                id="question3-desc",
                style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}}
            ),
            rx.radio_group(
                items=["ReLU (Rectified Linear Unit)", "Sigmoid", "Tanh", "All of the above"],
                default_value=State.answers[2],
                on_change=lambda answer: State.set_answers(answer, 2),
                color="black",
                id="question3-radio-group",
                **{
                    "aria-labelledby": "question3-label question3-desc",
                },
            ),
        ),
    )

def question4():
    return rx.vstack(
        rx.heading(
            "Question #4",
            color="black",
            style={"font-size": "20px", "@media (max-width: 768px)": {"font-size": "18px"}},
            id="question4-heading"
        ),
        rx.text(
            "What is the main goal of reinforcement learning?",
            color="black",
            as_="label",
            html_for="question4-radio-group",
            id="question4-label",
            style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
        ),
        rx.divider(**{"aria-hidden": "true"}),
        rx.box(
            rx.text(
                "Select the correct answer:",
                color="black",
                id="question4-desc",
                style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}}
            ),
            rx.radio_group(
                items=[
                    "To classify data into predefined categories",
                    "To learn a policy that maximizes cumulative rewards",
                    "To cluster data into groups",
                    "To reduce the dimensionality of data",
                ],
                default_value=State.answers[3],
                on_change=lambda answer: State.set_answers(answer, 3),
                color="black",
                id="question4-radio-group",
                **{
                    "aria-labelledby": "question4-label question4-desc",
                },
            ),
        ),
    )

def question5():
    return rx.vstack(
        rx.heading(
            "Question #5",
            color="black",
            style={"font-size": "20px", "@media (max-width: 768px)": {"font-size": "18px"}},
            id="question5-heading"
        ),
        rx.text(
            "Which of the following is a common application of Natural Language Processing (NLP)?",
            color="black",
            as_="label",
            html_for="question5-radio-group",
            id="question5-label",
            style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
        ),
        rx.divider(**{"aria-hidden": "true"}),
        rx.box(
            rx.text(
                "Select the correct answer:",
                color="black",
                id="question5-desc",
                style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}}
            ),
            rx.radio_group(
                items=["Sentiment Analysis", "Image Recognition", "Speech Recognition", "Both 1 and 3"],
                default_value=State.answers[4],
                on_change=lambda answer: State.set_answers(answer, 4),
                color="black",
                id="question5-radio-group",
                **{
                    "aria-labelledby": "question5-label question5-desc",
                },
            ),
        ),
    )


    
def render_answer(State, index):
    return rx.table.row(
        rx.table.cell(index + 1),
        rx.table.cell(
            rx.cond(
                State.answers[index].to_string() == State.answer_key[index].to_string(),
                rx.icon(tag="check", color="green"),
                rx.icon(tag="x", color="red"),
            )
        ),
        rx.table.cell(State.answers[index].to_string()),
        rx.table.cell(State.answer_key[index].to_string()),
    )


# Results component
def results():
    """The results view."""
    button_style = {
        "position": "relative",
        "display": "block",  # Full-width button
        "width": "100%",
        "text_align": "center",
        "font_size": "16px",
        "letter_spacing": "1px",
        "text_decoration": "none",
        "color": "#333333",
        "background": "#ffffff",
        "border": "3px solid #333333",
        "cursor": "pointer",
        "transition": "ease-out 0.5s",
        "border_radius": "0",
        "&:after": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "top": "-3px",
            "left": "-3px",
            "border_top": "3px solid transparent",
            "border_left": "3px solid transparent",
        },
        "&:before": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "bottom": "-3px",
            "right": "-3px",
            "border_bottom": "3px solid transparent",
            "border_right": "3px solid transparent",
        },
        "&:hover": {
            "color": "#333333",
            "text-decoration": "none",
        },
        "&:hover:after": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",  # Blue border on hover
        },
        "&:hover:before": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",  # Blue border on hover
        },
    }
    
    def centered_item(item):
        return rx.center(item, width="100%")

    def render_answer(answer, index):
        """Render a row in the results table."""
        return rx.table.row(
            rx.table.cell(index + 1),  # Question number
            rx.table.cell(
                rx.cond(
                    answer == State.answer_key[index],  # Condition
                    "✅",  # True case
                    "❌",  # False case
                )
            ),  # Result
            rx.table.cell(answer),  # User's answer
            rx.table.cell(State.answer_key[index]),  # Correct answer
        )

    return rx.center(
        rx.vstack(
            rx.heading("Results", color="black"),
            rx.text("Below are the results of the quiz.", color="black"),
            rx.divider(),
            rx.text(f"Your score: {State.percent_score}", color="black"),  # Display score as text
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("#", color="black"),
                        rx.table.column_header_cell("Result", color="black"),
                        rx.table.column_header_cell("Your Answer", color="black"),
                        rx.table.column_header_cell("Correct Answer", color="black"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(State.answers, lambda answer, index: render_answer(answer, index)),  # Render each answer
                ),
            ),
            centered_item(
                rx.hstack(
                    rx.link(
                        rx.button("Back to Home", style=button_style),  # Apply button_style
                        href="/",  # Link to the home page
                    ),
                    rx.link(
                        rx.button("Want to try a different quiz?", style=button_style),  # Apply button_style
                        href="https://www.proprofs.com/quiz-school/story.php?title=3dq-do-you-know-artificial-intelligence-ai",
                        target="_blank",  # Opens the link in a new tab
                    ),
                    spacing="2",  # Adds spacing between the buttons
                ),
            ),
            style=base_style,
        ),
        bg=page_background,
        min_height="100vh",
    )
    

def layout(content: rx.Component, breadcrumb_items: list[tuple[str, str]]) -> rx.Component:
    current_path = os.getenv("PAGE_PATH", "/")
    return rx.vstack(
        rx.html('<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>'),
        rx.html('<script src="https://kit.fontawesome.com/b89a958fe1.js" crossorigin="anonymous"></script>'),

        rx.script('''
            function initBackToTopButton() {
                var btn = $('#button');

                $(window).scroll(function() {
                    if ($(window).scrollTop() > 300) {
                        btn.addClass('show');
                    } else {
                        btn.removeClass('show');
                    }
                });

                btn.on('click', function(e) {
                    e.preventDefault();
                    $('html, body').animate({scrollTop:0}, '300');
                });
            }

            $(document).ready(function() {
                initBackToTopButton();
            });

            document.addEventListener('reflex:page:load', function() {
                initBackToTopButton();
            });
        '''),

        rx.html('''
            <style>
                .hover-link::after {
                    content: '';
                    display: block;
                    width: 0;
                    height: 2px;
                    background: #ff7f50;
                    transition: width .3s;
                }

                .hover-link:hover::after {
                    width: 100%;
                    transition: width .3s;
                }

                #button {
                    transition: opacity 0.3s ease;
                }
                #button.show {
                    opacity: 1 !important;
                }
            </style>
        '''),

        # Header section
        rx.box(
            rx.desktop_only(
                rx.hstack(
                    rx.hstack(
                        rx.heading("WebEducateAI", size="7", color="#F3F4F6", font_family="Montserrat", as_="h1"),
                        align_items="center",
                    ),
                    rx.hstack(
                        navbar_link("Home", "/", class_name="hover-link"),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.button(
                                    rx.text("Resources", size="4", weight="medium", color="white", font_family="Poppins"),
                                    rx.icon("chevron-down", color="white"),
                                    weight="medium", variant="ghost", size="3",
                                    aria_label="Resources menu"
                                ),
                            ),
                            rx.menu.content(
                                rx.menu.item(rx.link("User Experiences", href="/resources/user-experiences", color="white", font_family="Poppins", class_name="hover-link")),
                                rx.menu.item(rx.link("Educational Resources", href="/resources/educational-resources", color="white", font_family="Poppins", class_name="hover-link")),
                                rx.menu.item(rx.link("AI Academia", href="/resources/ai-academics", color="white", font_family="Poppins", class_name="hover-link")),
                                bg="#00bfff",  
                                border_radius="md", box_shadow="md",
                            ),
                        ),
                        navbar_link("Contact Us", "/contact-us", class_name="hover-link"),
                        navbar_link("About Us", "/about-us", class_name="hover-link"),
                        dark_mode_toggle(),
                        justify="end", spacing="5",
                    ),
                    justify="between", align_items="center",
                    as_="nav", role="navigation", aria_label="Main navigation"
                ),
            ),
            rx.mobile_and_tablet(
                rx.hstack(
                    rx.hstack(
                        rx.heading("WebEducateAI", size="7", color="white", font_family="Montserrat", as_="h1"),
                        align_items="center",
                    ),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.icon("menu", size=30, color="white"),
                        ),
                        rx.menu.content(
                            rx.menu.item(rx.link("Home", href="/", color="white", font_family="Poppins", class_name="hover-link")),
                            rx.menu.item(rx.link("User Experiences", href="/resources/user-experiences", color="white", font_family="Poppins", class_name="hover-link")),
                            rx.menu.item(rx.link("Educational Resources", href="/resources/educational-resources", color="white", font_family="Poppins", class_name="hover-link")),
                            rx.menu.item(rx.link("AI Academia", href="/resources/ai-academics", color="white", font_family="Poppins", class_name="hover-link")),
                            rx.menu.item(rx.link("Contact Us", href="/contact-us", color="white", font_family="Poppins", class_name="hover-link")),
                            rx.menu.item(rx.link("About Us", href="/about-us", color="white", font_family="Poppins", class_name="hover-link")),
                            rx.menu.item(dark_mode_toggle()),
                            bg="#00bfff", border_radius="md", box_shadow="md",
                        ),
                        justify="end",
                        aria_label="Mobile menu"
                    ),
                    justify="between", align_items="center",
                    as_="nav", role="navigation", aria_label="Mobile navigation"
                ),
            ),
            bg="#4b0082", padding="1em", width="100%", margin_top="-38px"
        ),

        breadcrumb_trail(breadcrumb_items),
        rx.cond(current_path == "/", TopBannerBasic.create(), None),

        # Main section
        rx.box(
            rx.vstack(
                content,
                spacing="4",
            ),
            as_="main", role="main",
            flex="1", width="100%", padding="2em",
            color=rx.cond(State.color_mode == "dark", "white", "black"),
            font_family="Poppins",
            background_color=rx.cond(State.color_mode == "dark", "#333333", "#F3F4F6"),
            display="flex", align_content="center",
            flex_direction="column", flex_wrap="wrap",
        ),

        # Back-to-top button with accessibility
        rx.box(
            rx.icon(tag="arrow-up", color="white", size=24),
            id="button",
            position="fixed", bottom="20px", right="20px",
            bg="#00bfff", padding="10px", border_radius="50%",
            box_shadow="md", _hover={"bg": "#009acd"},
            opacity="0", transition="opacity 0.3s ease",
            display="block", as_="button",
            role="button", aria_label="Back to top",
        ),

        background_color=rx.cond(State.color_mode == "dark", "#333333", "#F3F4F6"),
    )

def navbar_link(text: str, href: str, class_name: str = "") -> rx.Component:
    return rx.link(
        text,
        href=href,
        color="white",
        font_family="Poppins",
        class_name=class_name,
        _hover={"text_decoration": "none"},
        role="link",
        aria_label=f"Navigate to {text} page"
    )
    

def home() -> rx.Component:
    # Reflex icons
    icons = [
        "brain",  # Brain icon for Introduction to AI
        "cpu",  # CPU icon for Machine Learning Basics
        "circuit_board",  # Circuit board icon for Deep Learning Explained
    ]

    # Custom CSS for the hover effect
    hover_effect_style = {
        "display": "inline-block",
        "padding_top": "10px",
        "padding_bottom": "5px",
        "position": "relative",
        "overflow": "hidden",
        "color": "blue",  
        "transition": "color 0.3s ease",  # Smooth transition for text color
        "text-decoration": "none",
        "&:before": {
            "content": '""',
            "position": "absolute",
            "left": "0",
            "bottom": "0",
            "width": "100%",
            "height": "2px",
            "background": "purple",  # Color of the underline
            "transform": "translateX(-100%)",
            "transition": "transform 0.3s ease",
        },
        "&:hover": {
            "color": "purple",  # Text color on hover
        },
        "&:hover:before": {
            "transform": "translateX(0)",  # Slide in the underline
        },
    }
    
    button_style = {
        "position": "relative",
        "display": "block",  # Change to block to span full width
        "width": "100%",  # Make the button span the full width
        "text_align": "center",
        "font_size": "16px",
        "letter_spacing": "1px",
        "text_decoration": "none",
        "color": "#333333",
        "background": "#ffffff",
        "border": "3px solid #333333",
        "cursor": "pointer",
        "transition": "ease-out 0.5s",
        "border_radius": "0",
        "&:after": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "top": "-3px",
            "left": "-3px",
            "border_top": "3px solid transparent",
            "border_left": "3px solid transparent",
        },
        "&:before": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "bottom": "-3px",
            "right": "-3px",
            "border_bottom": "3px solid transparent",
            "border_right": "3px solid transparent",
        },
        "&:hover": {
            "color": "#333333",
        },
        "&:hover:after": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
        "&:hover:before": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
    }

    return layout(
    rx.box(
        rx.box(  # Main content container
            rx.vstack(
                # Grid section with different icons
                rx.grid(
                    # Card 1 - Introduction to AI
                    rx.card(
                        rx.vstack(
                            rx.icon(tag=icons[0], size=50, color="black", aria_label="Artificial Intelligence icon"),
                            rx.heading("Introduction To AI", size="4", margin_top="0.5rem", color="#333333"),
                            rx.text(
                                "Explore what Artificial Intelligence is, its history, and its real-world applications.",
                                font_size="16px",
                                padding="0.5rem",
                                color="#333333",
                                aria_label="Description of Introduction to AI content",
                            ),
                            rx.dialog.root(
                                rx.dialog.trigger(
                                    rx.button(
                                        "Open Dialog",
                                        style=button_style,
                                        aria_label="Open Introduction to AI references dialog",
                                        id="intro-ai-dialog-trigger"
                                    )
                                ),
                                rx.dialog.content(
                                    rx.box(
                                        rx.heading(
                                            "Useful References: Introduction to AI",
                                            size="4",
                                            color="white",
                                            text_align="center",
                                            padding="1rem",
                                            margin="0",
                                            font_family="Montserrat",
                                            aria_level="2"
                                        ),
                                        background_color="#4b0082",
                                        border_top_left_radius="15px",
                                        border_top_right_radius="15px",
                                        width="100%",
                                    ),
                                    rx.table.root(
                                        rx.table.header(
                                            rx.table.row(
                                                rx.table.column_header_cell("Paper Title", scope="col"),
                                                rx.table.column_header_cell("URL", scope="col"),
                                                rx.table.column_header_cell("Download PDF", scope="col"),
                                            ),
                                        ),
                                        rx.table.body(
                                            rx.table.row(
                                                rx.table.row_header_cell("AI in History", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://shorturl.at/zt5De", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View AI in History paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_history.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download AI in History PDF"
                                                    ),
                                                ),
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell("The Ethics of AI Ethics: An Evaluation of Guidelines", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://shorturl.at/o4Nsk", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Ethics of AI Ethics paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_ethics.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download Ethics of AI Ethics PDF"
                                                    ),
                                                ),
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell("Research Paper on Artificial Intelligence & its Applications", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://ijrti.org/papers/IJRTI2304061.pdf", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Research Paper on AI Applications")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_research.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download AI Research PDF"
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width="100%",
                                        margin_top="1rem",
                                        role="grid",
                                        aria_label="Introduction to AI references table"
                                    ),
                                    rx.dialog.close(
                                        rx.button("Close Dialog", style=button_style,
                                                aria_label="Close Introduction to AI references dialog")
                                    ),
                                    height="auto",
                                    padding="1rem",
                                    background_color="white",
                                    border_radius="15px",
                                    role="dialog",
                                    aria_labelledby="intro-ai-dialog-trigger"
                                ),
                            ),
                            spacing="1",
                            align="center",
                        ),
                        padding="1rem",
                        bg="orange.400",
                        border_radius="15px",
                        shadow="5px",
                        width="250px",
                        height="auto",
                        role="region",
                        aria_label="Introduction to AI card"
                    ),

                    # Card 2 - Machine Learning Basics
                    rx.card(
                        rx.vstack(
                            rx.icon(tag=icons[1], size=50, color="black", aria_label="Machine Learning icon"),
                            rx.heading("Machine Learning Basics", size="4", margin_top="0.5rem", color="#333333"),
                            rx.text(
                                "Learn the fundamentals of Machine Learning, including key concepts like supervised and unsupervised learning.",
                                font_size="16px",
                                padding="0.5rem",
                                color="#333333",
                                aria_label="Description of Machine Learning Basics content",
                            ),
                            rx.dialog.root(
                                rx.dialog.trigger(
                                    rx.button(
                                        "Open Dialog",
                                        style=button_style,
                                        aria_label="Open Machine Learning Basics references dialog",
                                        id="ml-dialog-trigger"
                                    )
                                ),
                                rx.dialog.content(
                                    rx.box(
                                        rx.heading(
                                            "Useful References: Machine Learning Basics",
                                            size="4",
                                            color="white",
                                            text_align="center",
                                            padding="1rem",
                                            margin="0",
                                            font_family="Montserrat",
                                            aria_level="2"
                                        ),
                                        background_color="#4b0082",
                                        border_top_left_radius="15px",
                                        border_top_right_radius="15px",
                                        width="100%",
                                    ),
                                    rx.table.root(
                                        rx.table.header(
                                            rx.table.row(
                                                rx.table.column_header_cell("Paper Title", scope="col"),
                                                rx.table.column_header_cell("URL", scope="col"),
                                                rx.table.column_header_cell("Download PDF", scope="col"),
                                            ),
                                        ),
                                        rx.table.body(
                                            rx.table.row(
                                                rx.table.row_header_cell("Machine Learning: The Basics", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://link.springer.com/book/10.1007/978-981-16-8193-6", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Machine Learning Basics paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_machine_basics.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download Machine Learning Basics PDF"
                                                    ),
                                                ),
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell("Machine Learning: Algorithms, Real-World Applications and Research Directions", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://link.springer.com/article/10.1007/s42979-021-00592-x", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Machine Learning Algorithms paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_machine_algorithms.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download Machine Learning Algorithms PDF"
                                                    ),
                                                ),
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell("Introduction to Machine Learning and Its Basic Application in Python", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3323796", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Machine Learning in Python paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_machine_python.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download Machine Learning in Python PDF"
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width="100%",
                                        margin_top="1rem",
                                        role="grid",
                                        aria_label="Machine Learning references table"
                                    ),
                                    rx.dialog.close(
                                        rx.button("Close Dialog", style=button_style,
                                                aria_label="Close Machine Learning references dialog")
                                    ),
                                    height="auto",
                                    padding="1rem",
                                    background_color="white",
                                    border_radius="15px",
                                    role="dialog",
                                    aria_labelledby="ml-dialog-trigger"
                                ),
                            ),
                            spacing="1",
                            align="center",
                        ),
                        padding="1rem",
                        bg="orange.400",
                        border_radius="15px",
                        shadow="5px",
                        width="250px",
                        height="auto",
                        role="region",
                        aria_label="Machine Learning Basics card"
                    ),

                    # Card 3 - Deep Learning Explained
                    rx.card(
                        rx.vstack(
                            rx.icon(tag=icons[2], size=50, color="black", aria_label="Deep Learning icon"),
                            rx.heading("Deep Learning Explained", size="4", margin_top="0.5rem", color="#333333"),
                            rx.text(
                                "Dive into Deep Learning, neural networks, and how they power advanced AI systems like image and speech recognition.",
                                font_size="16px",
                                padding="0.5rem",
                                color="#333333",
                                aria_label="Description of Deep Learning content",
                            ),
                            rx.dialog.root(
                                rx.dialog.trigger(
                                    rx.button(
                                        "Open Dialog",
                                        style=button_style,
                                        aria_label="Open Deep Learning references dialog",
                                        id="dl-dialog-trigger"
                                    )
                                ),
                                rx.dialog.content(
                                    rx.box(
                                        rx.heading(
                                            "Useful References: Deep Learning",
                                            size="4",
                                            color="white",
                                            text_align="center",
                                            padding="1rem",
                                            margin="0",
                                            font_family="Montserrat",
                                            aria_level="2"
                                        ),
                                        background_color="#4b0082",
                                        border_top_left_radius="15px",
                                        border_top_right_radius="15px",
                                        width="100%",
                                    ),
                                    rx.table.root(
                                        rx.table.header(
                                            rx.table.row(
                                                rx.table.column_header_cell("Paper Title", scope="col"),
                                                rx.table.column_header_cell("URL", scope="col"),
                                                rx.table.column_header_cell("Download PDF", scope="col"),
                                            ),
                                        ),
                                        rx.table.body(
                                            rx.table.row(
                                                rx.table.row_header_cell("Review of deep learning: concepts, CNN architectures, challenges, applications, future directions", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://journalofbigdata.springeropen.com/articles/10.1186/s40537-021-00444-8", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Deep Learning Concepts paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_deep_concepts.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download Deep Learning Concepts PDF"
                                                    ),
                                                ),
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell("Deep learning: systematic review, models, challenges, and research directions", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://link.springer.com/article/10.1007/s00521-023-08957-4", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Deep Learning Systematic Review paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_deep_systematic.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download Deep Learning Systematic Review PDF"
                                                    ),
                                                ),
                                            ),
                                            rx.table.row(
                                                rx.table.row_header_cell("Deep Learning: A Comprehensive Overview on Techniques, Taxonomy, Applications and Research Directions", scope="row"),
                                                rx.table.cell(
                                                    rx.link("View Paper", href="https://link.springer.com/article/10.1007/s42979-021-00815-1", is_external=True, 
                                                            color="blue", text_decoration="underline",
                                                            aria_label="View Deep Learning Comprehensive Overview paper")
                                                ),
                                                rx.table.cell(
                                                    rx.button(
                                                        "Download",
                                                        on_click=rx.download(url="/ai_deep_comprehensive.pdf"),
                                                        background_color="transparent",
                                                        color="darkgreen",
                                                        text_decoration="underline",
                                                        _hover={"color": "darkgreen"},
                                                        padding="0",
                                                        border="none",
                                                        cursor="pointer",
                                                        aria_label="Download Deep Learning Comprehensive Overview PDF"
                                                    ),
                                                ),
                                            ),
                                        ),
                                        width="100%",
                                        margin_top="1rem",
                                        role="grid",
                                        aria_label="Deep Learning references table"
                                    ),
                                    rx.dialog.close(
                                        rx.button("Close Dialog", style=button_style,
                                                aria_label="Close Deep Learning references dialog")
                                    ),
                                    height="auto",
                                    padding="1rem",
                                    background_color="white",
                                    border_radius="15px",
                                    role="dialog",
                                    aria_labelledby="dl-dialog-trigger"
                                ),
                            ),
                            spacing="1",
                            align="center",
                        ),
                        padding="1rem",
                        bg="orange.400",
                        border_radius="15px",
                        shadow="5px",
                        width="250px",
                        height="auto",
                        role="region",
                        aria_label="Deep Learning Explained card"
                    ),
                    gap="1rem",
                    grid_template_columns=["1fr", "repeat(2, 1fr)", "repeat(3, 1fr)"],
                    justify_content="center",
                ),
                
                # Heading and sub-heading section
                rx.vstack(
                    rx.heading("Want To See AI In Action?", size="6", color="#333333", margin_top="2rem", margin_bottom="0.5rem", aria_level="1"),
                    rx.heading("Then Look No Further", size="4", color="#666666", margin_bottom="2rem", aria_level="2"),
                    align="center",
                    width="100%",
                ),
                
                # Full-width grid with videos
                rx.grid(
                    # Card 1
                    rx.box(
                        rx.vstack(
                            rx.video(
                                url="https://www.youtube.com/watch?v=CiSaY2xl9V4",
                                width="100%",
                                height="200px",
                                controls=True,
                                autoplay=False,
                                loop=False,
                                title="Machine Learning Applications Video",
                                aria_label="Video showing real-world applications of machine learning"
                            ),
                            rx.text(
                                "Machine learning — the AI subfield in which machines learn from datasets and past experiences by recognizing patterns and generating predictions — is a $21B global industry, and it's projected to become a $209B industry by 2029. In this video, IBM Master Inventor Martin Keen shares some of the real-world applications of machine learning that have become part of our everyday lives",
                                font_size="16px",
                                padding="0.5rem",
                                color="#333333",
                            ),
                            spacing="1",
                            align="center",
                        ),
                        padding="1rem",
                        bg="orange.400",
                        border_radius="15px",
                        shadow="5px",
                        width="100%",
                        height="auto",
                        role="article",
                        aria_label="Machine Learning Applications video card"
                    ),
                    
                    # Card 2
                    rx.box(
                        rx.vstack(
                            rx.video(
                                url="https://www.youtube.com/watch?v=okzIOEPiHM0",
                                width="100%",
                                height="200px",
                                controls=True,
                                autoplay=False,
                                loop=False,
                                title="Generative AI Use Cases Video",
                                aria_label="Video showing 10 real-world generative AI examples"
                            ),
                            rx.text(
                                "You have to admit there is lots of hype around generative AI and it can seem that this latest buzzword is little more than marketing and hot air. But there are actually many real world use cases where generative AI is doing good. In this video I want to look at 10 real world gen-AI examples, without the hype and without the nonsense!",
                                font_size="16px",
                                padding="0.5rem",
                                color="#333333",
                            ),
                            spacing="1",
                            align="center",
                        ),
                        padding="1rem",
                        bg="orange.400",
                        border_radius="15px",
                        shadow="5px",
                        width="100%",
                        height="auto",
                        role="article",
                        aria_label="Generative AI Use Cases video card"
                    ),
                    
                    # Card 3
                    rx.box(
                        rx.vstack(
                            rx.video(
                                url="https://www.youtube.com/watch?v=_IOh0S_L3C4",
                                width="100%",
                                height="200px",
                                controls=True,
                                autoplay=False,
                                loop=False,
                                title="AI Limitations Video",
                                aria_label="Video discussing limitations of current AI systems"
                            ),
                            rx.text(
                                "From GPUs burning through billions of dollars to the surprising limitations of large language models, we'll dive deep into why AI struggles with reasoning, creativity, and real-world problem-solving. But it's not over yet—new breakthroughs might find a way around this roadblock. Is AI truly capped, or is there another paradigm shift on the horizon? Let's find out",
                                font_size="16px",
                                padding="0.5rem",
                                color="#333333",
                            ),
                            spacing="1",
                            align="center",
                        ),
                        padding="1rem",
                        bg="orange.400",
                        border_radius="15px",
                        shadow="5px",
                        width="100%",
                        height="auto",
                        role="article",
                        aria_label="AI Limitations video card"
                    ),
                    gap="0",
                    grid_template_columns=["1fr", "repeat(2, 1fr)", "repeat(3, 1fr)"],
                    width="100%",
                ),
                align="center",
                width="100%",
            ),
            role="main",
            aria_label="Main content section"
        ),
        display="flex",
        align_items="center",
        justify_content="center",
        width="100%",
        background_color="#F3F4F6",
    ),
        breadcrumb_items=[("Home", "/")],
        
    )
  
def timeline() -> rx.Component:
    return rx.box(
        rx.foreach(
            rx.Var.range(5),  # Generates 5 timeline cards
            lambda i: rx.box(
                rx.box(
                    # Individual heading for each timeline item
                    rx.heading(
                        rx.cond(
                            i == 0, "Rule-Based Systems (1950s - 1980s)",
                            rx.cond(
                                i == 1, "Machine Learning (1990s - Early 2000s)",
                                rx.cond(
                                    i == 2, "Deep Learning and Neural Networks (2010s - Present)",
                                    rx.cond(
                                        i == 3, "Reinforcement Learning and Autonomous Systems (2015 - Present)",
                                        rx.cond(
                                            i == 4, "General AI and Ethical Considerations (Future)",
                                            "General AI and Ethical Considerations (Future)"  # Default for anything else
                                        )
                                    )
                                )
                            )
                        ),
                        class_name="title",
                        style={"font-size": "24px", "@media (max-width: 768px)": {"font-size": "20px"}},
                        aria_level="2",  # Proper heading level for screen readers
                        id=f"timeline-heading-{i}",  # Unique ID for aria-labelledby
                    ),
                    # Individual text box for each timeline item
                    rx.text(
                        rx.cond(
                            i == 0, "The earliest AI systems were based on rule-based programming or expert systems...",
                            rx.cond(
                                i == 1, "In this stage, AI began evolving with machine learning (ML) techniques...",
                                rx.cond(
                                    i == 2, "The introduction of deep learning marked a revolutionary leap in AI...",
                                    rx.cond(
                                        i == 3, "During this phase, AI moved towards reinforcement learning (RL)...",
                                        rx.cond(
                                            i == 4, "The next stage in AI's evolution is General AI, or AGI...",
                                            "General AI and Ethical Considerations (Future)"
                                        )
                                    )
                                )
                            )
                        ),
                        class_name="info",
                        style={"font-size": "16px", "@media (max-width: 768px)": {"font-size": "14px"}},
                        aria_labelledby=f"timeline-heading-{i}",  # Associate text with heading
                        role="region",  # Landmark role for screen readers
                        tab_index=0,  # Make content focusable for keyboard users
                    ),
                    class_name="info",
                    role="article",  # Each timeline item is a self-contained article
                    aria_label=f"AI Evolution Timeline Item {i+1} of 5",  # Context for screen readers
                ),
                class_name=rx.cond((i % 2) == 0, "card even", "card odd"),
                role="listitem",  # Each item is part of a list
                aria_posinset=str(i+1),  # Position in set (1-based index)
                aria_setsize="5",  # Total number of items in the set
                tab_index=0,  # Make each item focusable
            ),
        ),
        class_name="timeline",
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
        role="list",  # Main container is a list
        aria_label="AI Evolution Timeline",  # Label for the entire timeline
        tab_index=0,  # Make timeline focusable
    )



    
def ux() -> rx.Component:
    button_style = {
        "position": "relative",
        "display": "block",
        "width": "100%",
        "text_align": "center",
        "font_size": "16px",
        "letter_spacing": "1px",
        "text_decoration": "none",
        "color": "#333333",
        "background": "#ffffff",
        "border": "3px solid #333333",
        "cursor": "pointer",
        "transition": "ease-out 0.5s",
        "border_radius": "0",
        "&:after": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "top": "-3px",
            "left": "-3px",
            "border_top": "3px solid transparent",
            "border_left": "3px solid transparent",
        },
        "&:before": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "bottom": "-3px",
            "right": "-3px",
            "border_bottom": "3px solid transparent",
            "border_right": "3px solid transparent",
        },
        "&:hover": {
            "color": "#333333",
        },
        "&:hover:after": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
        "&:hover:before": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
    }

    return layout(
    rx.box(
        rx.vstack(
            timeline(),
            rx.center(
                rx.vstack(
                    header(),
                    rx.form(  # Wrap the questions in a form element
                        rx.vstack(
                            question1(),
                            rx.divider(**{"aria-hidden": "true"}),
                            question2(),
                            rx.divider(**{"aria-hidden": "true"}),
                            question3(),
                            rx.divider(**{"aria-hidden": "true"}),
                            question4(),
                            rx.divider(**{"aria-hidden": "true"}),
                            question5(),
                            rx.center(
                                rx.button(
                                    "Submit",
                                    style=button_style,
                                    width="6em",
                                    on_click=State.submit,
                                    aria_label="Submit quiz answers",
                                    id="quiz-submit-button",
                                    type="submit",  # Proper form submission
                                    tab_index=0,
                                ),
                                width="100%",
                            ),
                            style=question_style,
                            spacing="5",
                            class_name="quiz-form",
                            id="quiz-form",
                            role="form",
                            aria_labelledby="quiz-header",
                        ),
                        on_submit=State.submit,  # Handle form submission
                    ),
                    align="center",
                    background_color="white",
                    padding="20px",
                    border_radius="10px",
                    box_shadow="0 4px 8px rgba(0, 0, 0, 0.2)",
                    role="region",
                    aria_label="User Experience Quiz Section",
                    id="quiz-section",  # Added ID for reference
                ),
                bg=page_background,
                padding_y="2em",
                min_height="100vh",
                role="main",
            ),
            justify_content="center",
            align_items="center",
            spacing="4",
            role="complementary",
            aria_label="AI Evolution Timeline",
        ),
        role="article",
        aria_label="User Experience Research Section",
        ),
        breadcrumb_items=[
            ("Home", "/"),
            ("Quiz", "/quiz"),
        ],
    )
   

def educational() -> rx.Component:
    return layout(
        rx.vstack(
            rx.heading(
                "Educational Resources on AI", 
                font_size="2.5em", 
                color="#4b0082", 
                margin_bottom="20px",
                id="main-heading",
                aria_level="1",
            ),
            rx.text(
                "Explore the fascinating world of Artificial Intelligence through curated resources, interactive tools, and learning materials.", 
                font_size="1.2em", 
                color="#666", 
                margin_bottom="40px",
                aria_labelledby="main-heading",
            ),

            # Section 1: What is AI?
            rx.box(
                rx.heading(
                    "What is Artificial Intelligence?", 
                    font_size="2em", 
                    color="#4b0082", 
                    margin_bottom="10px",
                    aria_level="2",
                    id="what-is-ai-heading",
                ),
                rx.text(
                    "Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think, learn, and make decisions. "
                    "From self-driving cars to virtual assistants, AI is transforming industries and everyday life.",
                    font_size="1.1em", 
                    color="#444", 
                    margin_bottom="20px",
                    aria_labelledby="what-is-ai-heading",
                ),
                padding="20px",
                border="1px solid #ddd",
                border_radius="10px",
                margin_bottom="40px",
                background_color="#ffffff",
                role="region",
                aria_label="What is Artificial Intelligence section",
            ),

            # Section 2: AI Learning Resources
            rx.box(
                rx.heading(
                    "AI Learning Resources", 
                    font_size="2em", 
                    color="#4b0082", 
                    margin_bottom="10px",
                    aria_level="2",
                    id="resources-heading",
                ),
                rx.text(
                    "Here are some great resources to get started with AI:",
                    font_size="1.1em", 
                    color="#444", 
                    margin_bottom="20px",
                    aria_labelledby="resources-heading",
                ),
                rx.grid(
                    *[
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.image(
                                        src=img_url,
                                        alt=f"Decorative image representing: {title}",
                                        width="250px",  # Original fixed width
                                        height="200px",
                                        object_fit="cover",
                                        border_radius="10px 10px 0 0",
                                        class_name="hover:scale-110 transition-transform duration-400 ease-in-out",
                                        loading="lazy",
                                        decoding="async",
                                    ),
                                    role="img",
                                    aria_label=f"Visual representation of {title}",
                                    width="250px",  # Matching container width
                                    height="200px",
                                    overflow="hidden",
                                ),
                                rx.box(
                                    rx.heading(
                                        title, 
                                        font_size="1.5em", 
                                        color="#4b0082", 
                                        margin_bottom="10px",
                                        class_name="transition-colors duration-300 ease-out hover:text-[#4b0082]",
                                        aria_level="3",
                                    ),
                                    rx.text(
                                        desc,
                                        color="#666",
                                        margin_bottom="20px",
                                    ),
                                    rx.spacer(),
                                    rx.link(
                                        rx.hstack(
                                            rx.text(
                                                "Read more about this topic",
                                                color="#4b0082",
                                                class_name="hover:text-[#4b0082]",
                                            ),
                                            rx.icon(tag="arrow-right", color="#4b0082", margin_left="8px")
                                        ),
                                        href=link,
                                        text_decoration="none",
                                        is_external=True,
                                        _hover={"text_decoration": "underline"},
                                        _focus={
                                            "outline": "2px solid #4b0082",
                                            "outline_offset": "2px",
                                        },
                                        aria_label=f"Read more about {title} (opens in new tab)",
                                        role="button",
                                        tab_index=0,
                                    ),
                                    padding="20px",
                                    flex="1",
                                    display="flex",
                                    flex_direction="column",
                                    width="250px", 
                                ),
                            ),
                            border="1px solid #ddd",
                            border_radius="10px",
                            overflow="hidden",
                            class_name="hover:shadow-lg hover:shadow-[rgba(0,0,0,0.16)] transition-all duration-400 ease-in-out",
                            background_color="#ffffff",
                            height="100%",
                            display="flex",
                            flex_direction="column",
                            role="article",
                            aria_label=f"Resource: {title}",
                            tab_index=0,
                            width="250px"  
                        ) for title, desc, img_url, link in [
                            ("Introduction to AI", "Learn the basics of Artificial Intelligence...", "https://wallpaperaccess.com/full/4915631.png", "https://openlearning.mit.edu/news/explore-world-artificial-intelligence-online-courses-mit"),
                            ("Machine Learning Basics", "Discover the fundamentals of Machine Learning...", "https://wallpaperaccess.com/full/3079643.jpg", "https://developers.google.com/machine-learning/crash-course"),
                            ("Deep Learning Explained", "Explore Deep Learning, neural networks...", "https://wallpaperaccess.com/full/3079568.jpg", "https://365datascience.com/trending/what-is-deep-learning/")
                        ]
                    ],
                    columns={"base": "1", "md": "2", "lg": "3"},
                    spacing="4",
                    role="list",
                    aria_label="List of AI learning resources",
                    justify_content="center,"  # Center the grid items
                ),
                padding="20px",
                border="1px solid #ddd",
                border_radius="10px",
                margin_bottom="40px",
                background_color="#ffffff",
                role="region",
                aria_label="AI Learning Resources section",
                width="100%",
            ),
            spacing="4",
            padding="40px",
            background_color="#f3f4f6",
            role="main",
        ),
        breadcrumb_items=[
            ("Home", "/"),
            ("Resources", "/resources"),
            ("Educational Resources", "/resources/educational-resources")
        ]
    )
    



    
def about() -> rx.Component:
    return layout(
        rx.box(
            rx.vstack(
                rx.box(
                    rx.vstack(
                        rx.heading(
                            "About Us",
                            font_size="2em",
                            font_weight="900",
                            margin_bottom="30px",
                            color="#333333",
                            id="about-heading",
                            aria_level=1,
                        ),
                        rx.text(
                            "Welcome to WebEducateAI, your gateway to understanding and harnessing the power of artificial intelligence. "
                            "We are dedicated to making AI education accessible, engaging, and insightful for learners of all backgrounds—"
                            "whether you're a curious beginner or an experienced professional.",
                            font_size="0.9em", 
                            color="#333333", 
                            line_height="30px", 
                            margin_bottom="20px",
                            aria_labelledby="about-heading",
                        ),
                        rx.text(
                            "Our mission is to demystify AI by providing clear, well-structured resources. "
                            "Through content designed for the users, we empower them to explore AI's potential with confidence.",
                            font_size="0.9em", 
                            color="#333333", 
                            line_height="30px", 
                            margin_bottom="20px",
                        ),
                        rx.text(
                            "At WebEducateAI, we believe knowledge should be both accessible and adaptable. "
                            "That's why we incorporate customizable accessibility features, ensuring an inclusive learning experience for everyone. "
                            "Our interactive approach encourages curiosity, critical thinking, helping you stay ahead in the rapidly evolving world of AI.",
                            font_size="0.9em", 
                            color="#333333", 
                            line_height="30px", 
                            margin_bottom="20px",
                        ),
                        rx.text(
                            "Join us on this journey to explore, learn, and shape the future of AI—one discovery at a time.",
                            font_size="0.9em", 
                            color="#333333", 
                            line_height="30px", 
                            margin_bottom="40px",
                        ),
                        align="start",
                        padding="150px",
                        width="55%",
                        float="right",
                        background_color="#fdfdfd",
                        role="region",
                        aria_label="About WebEducateAI content",
                        tab_index=0,
                    ),
                    width="100%",
                    overflow="hidden",
                    role="complementary",
                ),
                align="center",
                width="100%",
                padding="100px 0",
                background_image="url(https://wallpaperaccess.com/full/2091384.jpg)",
                background_position="left",
                background_size="55%",
                background_repeat="no-repeat",
                background_color="#fdfdfd",
                aria_label="About page background section",
            ),
            width="100%",
            role="main",
        ),
        breadcrumb_items=[
            ("Home", "/"),
            ("About Us", "/about-us")
        ],
    )



def contact() -> rx.Component:
    button_style = {
        "position": "relative",
        "display": "block",
        "width": "100%",
        "text_align": "center",
        "font_size": "16px",
        "letter_spacing": "1px",
        "text_decoration": "none",
        "color": "#333333",
        "background": "#ffffff",
        "border": "3px solid #333333",
        "cursor": "pointer",
        "transition": "ease-out 0.5s",
        "border_radius": "0",
        "&:after": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "top": "-3px",
            "left": "-3px",
            "border_top": "3px solid transparent",
            "border_left": "3px solid transparent",
        },
        "&:before": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "bottom": "-3px",
            "right": "-3px",
            "border_bottom": "3px solid transparent",
            "border_right": "3px solid transparent",
        },
        "&:hover": {
            "color": "#333333",
        },
        "&:hover:after": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
        "&:hover:before": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
    }

    def form_field(label_text, field_name, input_component, **kwargs):
        """Helper to create properly associated form fields"""
        return rx.form.field(
            rx.flex(
                rx.form.label(
                    label_text,
                    html_for=field_name,
                    class_name="form-label",
                ),
                input_component(
                    id=field_name,
                    name=field_name,
                    class_name=kwargs.get("class_name", "form-input"),
                    color="#333333",
                    border_color="#333333",
                    required=True,
                    **{k: v for k, v in kwargs.items() if k != "class_name"}
                ),
                direction="column",
                spacing="2",
            ),
            name=field_name,
        )

    return layout(
        rx.vstack(
            rx.heading(
                "Suggest Improvements", 
                size="2", 
                class_name="contact-title", 
                color="#333333", 
                font_weight="bold",
                id="contact-heading",
                aria_level=1,
            ),
            rx.text(
                "Have ideas for new features or improvements? Let us know how we can make this website better for you!", 
                class_name="subtitle", 
                color="#333333",
                aria_labelledby="contact-heading",
            ),
            rx.form.root(
                rx.vstack(
                    rx.hstack(
                        # Name Field
                        form_field(
                            "Your Name",
                            "name",
                            rx.input,
                            placeholder="Enter your name",
                            on_change=ContactFormState.set_name
                        ),
                        # Email Field
                        form_field(
                            "Your Email",
                            "email",
                            lambda **kw: rx.input(type="email", **kw),
                            placeholder="Enter your email",
                            on_change=ContactFormState.set_email
                        ),
                        spacing="2",
                    ),
                    rx.hstack(
                        # Subject Field
                        form_field(
                            "Suggested Change",
                            "subject",
                            rx.input,
                            placeholder="Feature or improvement idea",
                            on_change=ContactFormState.set_subject
                        ),
                        # Priority Field
                        form_field(
                            "Priority Level",
                            "priority",
                            lambda **kw: rx.select(items=["Low", "Medium", "High"], **kw),
                            placeholder="Select priority",
                            on_change=ContactFormState.set_contact
                        ),
                        spacing="2",
                    ),
                    # Details Field
                    form_field(
                        "Details",
                        "issue",
                        lambda **kw: rx.text_area(rows="4", **kw),
                        placeholder="Describe your suggestion",
                        on_change=ContactFormState.set_issue,
                        class_name="form-textarea"
                    ),
                    rx.box(
                        rx.form.submit(
                            rx.button("Submit Suggestion", style=button_style),
                            as_child=True,
                        ),
                        width="100%",
                        display="flex",
                        justify_content="center",
                    ),
                    spacing="4",
                ),
                on_submit=ContactFormState.handle_submit,
                reset_on_submit=False,
            ),
            rx.cond(
                ContactFormState.status,
                rx.box(
                    rx.text(
                        ContactFormState.status,
                        color=rx.cond(
                            ContactFormState.status.contains("success"),
                            "green",
                            "red",
                        ),
                        font_weight="bold",
                    ),
                    padding="10px",
                    border_radius="5px",
                    background=rx.cond(
                        ContactFormState.status.contains("success"),
                        "#f0fff4",
                        "#fff0f0",
                    ),
                    border=rx.cond(
                        ContactFormState.status.contains("success"),
                        "1px solid green",
                        "1px solid red",
                    ),
                    role="alert",
                    aria_live="polite",
                ),
            ),
            spacing="6",
            style={
                "width": "90%",
                "max-width": "600px",
                "padding": "40px",
                "background-color": "#f3f4f6",
                "box-shadow": "0 8px 16px rgba(0, 0, 0, 0.2)",
                "animation": "fadeIn 1s ease-out",
            },
            align_items="center",
            justify_content="center",
            height="100vh",
            role="main",
            aria_label="Contact form section",
        ),
        breadcrumb_items=[
            ("Home", "/"),
            ("Contact Us", "/contact"),
        ],
    )
    
def sad_face_emoji():
    return rx.text("😢", font_size="1em", margin_left="0.3em", as_="span")

def custom_404() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.text("404", class_name="glitch", data_text="404", font_size="4em", font_weight="bold"),
            rx.text(
                "Looks like you're lost! ",
                sad_face_emoji(),  # Embed the emoji inline
                class_name="message",
            ),
            rx.link("Go home?", href="/", style={
                    "color": "#00bfff",
                    "text_decoration": "none",
                    "transition": "0.3s",
                    "font_family": "Lora, serif",
            }),
            spacing="2",
            align="center",
        ),
        height="100vh",
        background="radial-gradient(circle, #1a1a1a, #000)",
    )
    
def academics() -> rx.Component:
    button_style = {
        "position": "relative",
        "display": "block",
        "width": "100%",
        "text_align": "center",
        "font_size": "16px",
        "letter_spacing": "1px",
        "text_decoration": "none",
        "color": "#333333",
        "background": "#ffffff",
        "border": "3px solid #333333",
        "cursor": "pointer",
        "transition": "ease-out 0.5s",
        "border_radius": "0",
        "&:after": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "top": "-3px",
            "left": "-3px",
            "border_top": "3px solid transparent",
            "border_left": "3px solid transparent",
        },
        "&:before": {
            "position": "absolute",
            "content": '""',
            "width": "0",
            "height": "0",
            "transition": "0.5s",
            "bottom": "-3px",
            "right": "-3px",
            "border_bottom": "3px solid transparent",
            "border_right": "3px solid transparent",
        },
        "&:hover": {
            "color": "#333333",
        },
        "&:hover:after": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
        "&:hover:before": {
            "width": "calc(50% + 3px)",
            "height": "calc(50% + 3px)",
            "border_color": "#00bfff",
        },
    }
    
    articles = [
        {"title": "Proliferation of AI Tools: A Multifaceted Evaluation"},
        {"title": "The Impact of AI on Web Development"},
        {"title": "Web Evolution to Revolution: Navigating the Future of Web Application Development"},
    ]

    return layout(
        breadcrumb_items=[
            ("Home", "/"),
            ("Resources", "/resources"),
            ("AI Academia", "/resources/ai-academics"),
        ],
        content=rx.vstack(
            rx.heading(
                "AI Academic Papers",
                size="4",
                margin_bottom="1em",
                id="academic-papers-heading",
                aria_level=1,
            ),
            *[
                rx.box(
                    rx.hstack(
                        # Left Column (2/3 width) - Paper Details Section
                        rx.box(
                            rx.vstack(
                                rx.heading(
                                    f"Paper Title: {title}",
                                    size="3",
                                    id=f"paper-title-{i}",
                                    aria_level=2,
                                ),
                                rx.text(
                                    f"Abstract: {abstract}",
                                    aria_labelledby=f"paper-title-{i}",
                                ),
                                rx.text(
                                    f"Keywords: {keywords}",
                                    aria_labelledby=f"paper-title-{i}",
                                ),
                                spacing="4",
                                padding="4",
                                border="1px solid #e2e8f0",
                                border_radius="lg",
                                box_shadow="md",
                            ),
                            width="66%",
                            role="region",
                            aria_label=f"Details for {title}",
                        ),
                        # Right Column (1/3 width) - PDF Download Section
                        rx.box(
                            rx.vstack(
                                rx.box(
                                    rx.image(
                                        src=img_src,
                                        alt=f"Preview image for {title}",
                                        border_radius="md",
                                        box_shadow="lg",
                                        width="100%",
                                        role="img",
                                    ),
                                ),
                                rx.button(
                                    f"Download PDF ({file_size}MB)",
                                    on_click=rx.download(url=pdf_url),
                                    style=button_style,
                                    aria_label=f"Download PDF of {title}",
                                    tab_index=0,
                                ),
                                align="center",
                                spacing="4",
                                padding="4",
                                border="1px solid #e2e8f0",
                                border_radius="lg",
                                box_shadow="md",
                            ),
                            width="33%",
                            role="complementary",
                            aria_label=f"Download options for {title}",
                        ),
                        spacing="8",
                        align="start",
                        width="100%",
                    ),
                    role="article",
                    aria_label=f"Academic paper: {title}",
                    margin_bottom="2em",
                ) for i, (title, abstract, keywords, img_src, pdf_url, file_size) in enumerate([
                    ("Proliferation of AI Tools: A Multifaceted Evaluation", 
                     "This study examines the impact of AI tools...", 
                     "AI tools shape jobs, performance, ethics...", 
                     "/ai_tools_image.PNG", "/ai_tools.pdf", 0.4),
                    ("The Impact of AI on Web Development", 
                     "This paper examines the impact of AI on web development...", 
                     "Artificial Intelligence, Web Development...", 
                     "/ai_web_dev_image.PNG", "/ai_web_dev.pdf", 0.7),
                    ("Web Evolution to Revolution: Navigating the Future of Web Application Development", 
                     "This paper explores the evolution of web application development...", 
                     "This paper covers the evolution of web development...", 
                     "/ai_web_revolution_image.PNG", "/ai_web_revolution.pdf", 0.2)
                ])
            ],
            width="100%",
            padding="4",
            role="main",
            aria_labelledby="academic-papers-heading",
        ),
    )
    










    

    
    
app = rx.App(
    stylesheets=["/styles.css"],  # Correct way to load external CSS
    
)
app.add_page(home, route="/")
app.add_page(ux, route="/resources/user-experiences")
app.add_page(educational, route="/resources/educational-resources")
app.add_page(about, route="/about-us")      
app.add_page(contact, route="/contact-us")
app.add_page(results, route="/resources/educational-resources/result")
app.add_page(academics, route="/resources/ai-academics")
app.add_page(custom_404 , route="/404")







