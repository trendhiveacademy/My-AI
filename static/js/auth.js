// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyAghYlBpxqdaUg3V_J6QVjijJsoTusP5FA",
  authDomain: "trend-hive-s-ai.firebaseapp.com",
  projectId: "trend-hive-s-ai",
  storageBucket: "trend-hive-s-ai.appspot.com",
  messagingSenderId: "1009217669546",
  appId: "1:1009217669546:web:f6abde171dcf3e2b2cc3d3",
  measurementId: "G-RPBZ8XYR8F"
};

firebase.initializeApp(firebaseConfig);

// Google Login
async function signInWithGoogle() {
  const provider = new firebase.auth.GoogleAuthProvider();
  try {
    const result = await firebase.auth().signInWithPopup(provider);
    const user = result.user;
    console.log("Logged in:", user.displayName, user.email);

    // Send to Flask backend
    fetch("/save_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: user.displayName,
        email: user.email,
        uid: user.uid
      }),
    });
  } catch (error) {
    console.error("Login failed:", error.message);
  }
}
