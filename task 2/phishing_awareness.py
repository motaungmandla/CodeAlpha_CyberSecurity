import time

def print_slow(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def show_training_module():
    print("\n" + "="*50)
    print("🛡️  PHISHING AWARENESS TRAINING MODULE 🛡️")
    print("="*50)
    
    print_slow("\n MODULE 1: What is Phishing?")
    print("Phishing is a cyber attack where attackers disguise themselves as trustworthy entities (like banks or colleagues) to steal sensitive data like passwords and credit card numbers.")
    
    print_slow("\n📌 MODULE 2: How to Recognize Phishing Emails")
    print("1. 🚨 Urgent or threatening language (e.g., 'Your account will be suspended!')")
    print("2. 🔗 Suspicious links (hover over them to check the actual URL).")
    print("3.  Unexpected attachments (especially .exe, .zip, or macro-enabled docs).")
    print("4. ✉️ Generic greetings (e.g., 'Dear Customer' instead of your name).")
    
    print_slow("\n📌 MODULE 3: Social Engineering Tactics")
    print("Attackers use psychological manipulation. Common tactics include:")
    print("- Pretexting: Creating a fabricated scenario to steal info.")
    print("- Baiting: Offering something enticing (like a free USB drive).")
    print("- Quid Pro Quo: Requesting info in exchange for a benefit.")

def run_quiz():
    print("\n" + "="*50)
    print("🧠 INTERACTIVE QUIZ ")
    print("="*50)
    
    score = 0
    
    # Question 1
    print("\nQ1: You receive an email from 'PayPaI-Support@gmail.com' asking you to reset your password. What do you do?")
    print("A) Click the link and reset it immediately.")
    print("B) Ignore it and log in directly via the official PayPal website.")
    ans = input("Your answer (A/B): ").upper()
    if ans == 'B':
        print("✅ Correct! Always verify the sender and use official URLs.")
        score += 1
    else:
        print("❌ Incorrect! The email address is fake, and the link could be malicious.")

    # Question 2
    print("\nQ2: A colleague sends you a ZIP file named 'Urgent_Invoice.zip'. You weren't expecting an invoice. What do you do?")
    print("A) Open it to see what it is.")
    print("B) Contact the colleague via phone/Teams to verify before opening.")
    ans = input("Your answer (A/B): ").upper()
    if ans == 'B':
        print("✅ Correct! Always verify unexpected attachments out-of-band.")
        score += 1
    else:
        print("❌ Incorrect! It could contain ransomware or a trojan.")

    print(f"\n Quiz Complete! Your score: {score}/2")
    if score == 2:
        print("🌟 Excellent! You are Phishing-Proof!")
    else:
        print("📚 Review the training module above and try again!")

if __name__ == "__main__":
    show_training_module()
    run_quiz()
