const SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

const synth = window.speechSynthesis;

let systemStarted = false;
let stage = "idle";
let emailData = { to: "", subject: "", message: "" };

// SPEAK FUNCTION
function speak(text) {
  const u = new SpeechSynthesisUtterance(text);
  synth.speak(u);

  // Show what system speaks
  document.getElementById("transcript-text").innerText = text;
}

// UPDATE TRANSCRIPT
function update(text) {
  document.getElementById("transcript-text").innerText = text;
}

// START LISTENING
function startListening() {
  try {
    recognition.start();
  } catch {}
}

// START SYSTEM (Triggered by mic click)
function startSystem() {
  if (systemStarted) return;
  systemStarted = true;

  document.getElementById("status").innerText = "Listening… 🎧";
  speak("Welcome. Say compose email or read inbox.");
  startListening();
}

// AUTO RESTART LISTENING
recognition.onend = () => {
  if (systemStarted) {
    setTimeout(startListening, 700);
  }
};

// WHEN USER SPEAKS
recognition.onresult = (event) => {
  const text = event.results[0][0].transcript.toLowerCase();
  update("You said: " + text);

  // ---------------- READ INBOX ----------------
  if (text.includes("read inbox")) {
    speak("Reading your inbox");

    fetch("/read_inbox")
      .then(r => r.json())
      .then(d => {
        if (!d.emails || d.emails.length === 0) {
          speak("You have no new emails");
        } else {
          d.emails.forEach((e, index) => {
            speak(`Email ${index + 1}`);
            speak(`From ${e.from}`);
            speak(`Subject ${e.subject}`);
            speak(`Message ${e.body}`);
          });
        }
      })
      .catch(() => speak("Unable to read inbox"));

    return;
  }

  // ---------------- START COMPOSE ----------------
  if (stage === "idle" && text.includes("compose")) {
    stage = "to";
    speak("Please say the recipient email");
    return;
  }

  if (stage === "to") {
    emailData.to = normalizeEmail(text);
    stage = "subject";
    speak("Please say the subject");
    return;
  }

  if (stage === "subject") {
    emailData.subject = text;
    stage = "message";
    speak("Please say the message");
    return;
  }

  if (stage === "message") {
    emailData.message = text;
    stage = "confirm";
    speak("Do you want to send the email? Say yes or no.");
    return;
  }

  // ---------------- CONFIRMATION ----------------
  if (stage === "confirm") {
    if (text.includes("yes")) {
      speak("Sending email");
      sendEmail(emailData);
    } else {
      speak("Email cancelled");
    }

    stage = "idle";
    return;
  }

  // EXIT COMMAND
  if (text.includes("exit")) {
    speak("Goodbye");
    systemStarted = false;
    recognition.stop();
  }
};

// EMAIL NORMALIZER
function normalizeEmail(text) {
  return text
    .replace(/\s+/g, "")
    .replace(/at/gi, "@")
    .replace(/dot/gi, ".")
    .replace(/underscore/gi, "_")
    .replace(/dash/gi, "-")
    .replace(/one/gi, "1")
    .replace(/two/gi, "2")
    .replace(/three/gi, "3")
    .replace(/four/gi, "4")
    .replace(/five/gi, "5")
    .replace(/six/gi, "6")
    .replace(/seven/gi, "7")
    .replace(/eight/gi, "8")
    .replace(/nine/gi, "9")
    .replace(/zero/gi, "0");
}

// SEND EMAIL TO FLASK
function sendEmail(data) {
  fetch("/send_email", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then(r => r.json())
    .then(r => {
      speak(r.status);
      document.getElementById("status").innerText = r.status;
    })
    .catch(() => speak("Failed to send email"));
}