// Function to handle learning resource interactions
function startLearning(resource) {
    alert(`You selected: ${resource}. Get ready to dive into the material!`);
}

// Function to start a personalized learning pathway
function startPersonalizedPath() {
    alert("Starting your personalized learning pathway. Let us guide you!");
}

// Function to toggle high contrast mode
function toggleContrast() {
    document.body.classList.toggle("high-contrast");
}

// Form Submission Handling
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("contact-form");
    const messageBox = document.getElementById("form-message");

    if (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault(); // Prevent actual form submission

            const name = document.getElementById("name").value.trim();
            const email = document.getElementById("email").value.trim();
            const message = document.getElementById("message").value.trim();

            if (name === "" || email === "" || message === "") {
                messageBox.innerHTML = "Please fill in all fields.";
                messageBox.style.color = "red";
                return;
            }

            // Simulate form submission success
            messageBox.innerHTML = "Thank you for reaching out! We’ll get back to you soon.";
            messageBox.style.color = "green";

            // Reset form fields
            form.reset();
        });
    }
});



// AI Text Generator Simulation
function generateText() {
    const userInput = document.getElementById("ai-input").value.trim();
    const outputElement = document.getElementById("ai-output");

    if (userInput === "") {
        outputElement.innerText = "Please enter a topic!";
        outputElement.style.color = "red";
        return;
    }

    // Simulating AI-generated response
    const responses = [
        `AI is transforming the world of ${userInput} by improving efficiency and accuracy.`,
        `The future of ${userInput} is deeply connected to AI advancements.`,
        `With AI, ${userInput} is evolving at an unprecedented pace!`
    ];

    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    outputElement.innerText = randomResponse;
    outputElement.style.color = "green";
}

// AI Sentiment Analysis Simulation
function analyzeSentiment() {
    const userInput = document.getElementById("sentiment-input").value.trim();
    const outputElement = document.getElementById("sentiment-output");

    if (userInput === "") {
        outputElement.innerText = "Please enter a sentence!";
        outputElement.style.color = "red";
        return;
    }

    // Simulating a simple sentiment analysis
    const positiveWords = ["happy", "great", "excellent", "love", "amazing"];
    const negativeWords = ["sad", "bad", "terrible", "hate", "awful"];

    let sentiment = "Neutral";
    let color = "gray";

    for (let word of positiveWords) {
        if (userInput.toLowerCase().includes(word)) {
            sentiment = "Positive 😊";
            color = "green";
            break;
        }
    }

    for (let word of negativeWords) {
        if (userInput.toLowerCase().includes(word)) {
            sentiment = "Negative 😞";
            color = "red";
            break;
        }
    }

    outputElement.innerText = `Sentiment: ${sentiment}`;
    outputElement.style.color = color;
}


// FAQ Toggle Function
function toggleFAQ(index) {
    const answers = document.querySelectorAll(".faq-answer");
    const questions = document.querySelectorAll(".faq-question");

    if (answers[index].style.display === "block") {
        answers[index].style.display = "none";
        questions[index].innerHTML = questions[index].innerHTML.replace("▲", "▼");
    } else {
        answers[index].style.display = "block";
        questions[index].innerHTML = questions[index].innerHTML.replace("▼", "▲");
    }
}


// Toggle Learning Sections
function toggleTopic(index) {
    const topics = document.querySelectorAll(".topic-content");
    const buttons = document.querySelectorAll(".topic-title");

    if (topics[index].style.display === "block") {
        topics[index].style.display = "none";
        buttons[index].innerHTML = buttons[index].innerHTML.replace("▲", "▼");
    } else {
        topics[index].style.display = "block";
        buttons[index].innerHTML = buttons[index].innerHTML.replace("▼", "▲");
    }
}

// Function to toggle dark mode
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');  // Toggle dark mode class
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode')); // Save user preference
}

// Function to toggle color-blind mode
function toggleColorBlindMode() {
    document.body.classList.toggle('color-blind-mode');  // Toggle color-blind mode class
    localStorage.setItem('colorBlindMode', document.body.classList.contains('color-blind-mode')); // Save user preference
}

// Function to check the quiz answer
function checkAnswer(answer) {
    const feedbackElement = document.getElementById('quiz-feedback');
    if (answer === 'A') {
        feedbackElement.textContent = 'Correct! AI stands for Artificial Intelligence.';
    } else {
        feedbackElement.textContent = 'Incorrect. AI stands for Artificial Intelligence.';
    }
}

// Function to start learning a specific topic
function startLearning(topic) {
    alert(`Starting to learn about ${topic}`);  // Replace this with actual navigation or content loading logic
}

// On window load, check for saved preferences
window.onload = () => {
    // Check if dark mode was previously enabled
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }

    // Check if color-blind mode was previously enabled
    if (localStorage.getItem('colorBlindMode') === 'true') {
        document.body.classList.add('color-blind-mode');
    }
};

// Auto-Focus on First Input Field
window.onload = () => {
    document.getElementById('name').focus();
};

// Form Validation Feedback
const emailInput = document.getElementById('email');
emailInput.addEventListener('input', () => {
    if (!emailInput.checkValidity()) {
        emailInput.classList.add('invalid');
    } else {
        emailInput.classList.remove('invalid');
    }
});

// Character Counter for Textarea
const messageInput = document.getElementById('message');
const charCounter = document.getElementById('char-counter');

messageInput.addEventListener('input', () => {
    const charCount = messageInput.value.length;
    charCounter.textContent = `${charCount}/500`;
    if (charCount > 500) {
        charCounter.style.color = 'red';
    } else {
        charCounter.style.color = '#666';
    }
});

// Loading Spinner and Form Submission
const form = document.getElementById('contact-form');
const submitButton = form.querySelector('button[type="submit"]');
const formMessage = document.getElementById('form-message');

form.addEventListener('submit', (e) => {
    e.preventDefault();

    // Disable the submit button and show the spinner
    submitButton.disabled = true;
    submitButton.innerHTML = '<div class="spinner"></div> Sending...';

    // Simulate form submission delay
    setTimeout(() => {
        // Clear the form
        form.reset();
        charCounter.textContent = '0/500';

        // Show success message
        formMessage.textContent = 'Message sent successfully!';
        formMessage.classList.add('visible');

        // Re-enable the submit button
        submitButton.disabled = false;
        submitButton.innerHTML = 'Send Message';

        // Hide the message after 3 seconds
        setTimeout(() => {
            formMessage.classList.remove('visible');
        }, 3000);
    }, 2000);
});

