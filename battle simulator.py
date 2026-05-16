import tkinter as tk
from tkinter import messagebox
import random


# QUESTION BANK
class QuestionBank:

    def __init__(self):

        self.questions = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: []
        }

    def add_question(self, level, question, options, answer):

        self.questions[level].append({
            "question": question,
            "options": options,
            "answer": answer
        })

    def get_random_question(self, level):

        if len(self.questions[level]) == 0:
            raise ValueError("No more questions.")

        question = random.choice(self.questions[level])

        # REMOVE QUESTION SO IT NEVER REPEATS
        self.questions[level].remove(question)

        return question


# PLAYER STATS
class PlayerStats:

    def __init__(self, name):

        self.name = name
        self.health = 100
        self.score = 0

    def correct_answer(self):

        self.score += 10
        self.health += 5

        if self.health > 100:
            self.health = 100

    def wrong_answer(self):

        self.score -= 5
        self.health -= 10

        if self.health < 0:
            self.health = 0

    def get_stats(self):

        return (
            f"{self.name}\n"
            f"❤️ Health: {self.health}\n"
            f"⭐ Score: {self.score}"
        )


# MAIN APP
class App:

    def __init__(self, root, player_name):

        self.root = root
        self.root.title("⚔ Battle Simulator")
        self.root.geometry("1100x800")
        self.root.configure(bg="#121212")

        self.current_level = 1
        self.questions_answered = 0

        self.current_question = None

        self.question_bank = QuestionBank()

        self.player = PlayerStats(player_name)
        self.robot = PlayerStats("🤖 Robot Enemy")

        self.setup_questions()

        # TOP FRAME
        top_frame = tk.Frame(root, bg="#121212")
        top_frame.pack(pady=20)

        self.player_label = tk.Label(
            top_frame,
            text=self.player.get_stats(),
            font=("Arial", 16, "bold"),
            fg="#ffd54f",
            bg="#1e1e1e",
            width=20,
            height=5,
            relief="ridge",
            bd=5
        )

        self.player_label.grid(row=0, column=0, padx=50)

        self.vs_label = tk.Label(
            top_frame,
            text="⚔ VS ⚔",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#121212"
        )

        self.vs_label.grid(row=0, column=1, padx=30)

        self.robot_label = tk.Label(
            top_frame,
            text=self.robot.get_stats(),
            font=("Arial", 16, "bold"),
            fg="#ff5252",
            bg="#1e1e1e",
            width=20,
            height=5,
            relief="ridge",
            bd=5
        )

        self.robot_label.grid(row=0, column=2, padx=50)

        # COUNTER
        self.counter_label = tk.Label(
            root,
            text="LEVEL 1 | Questions: 0/20",
            font=("Arial", 16, "bold"),
            fg="#80d8ff",
            bg="#121212"
        )

        self.counter_label.pack(pady=10)

        # QUESTION LABEL
        self.question_label = tk.Label(
            root,
            text="Loading Questions...",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#121212",
            wraplength=1000,
            justify="center"
        )

        self.question_label.pack(pady=30)

        # OPTIONS FRAME
        self.options_frame = tk.Frame(
            root,
            bg="#121212"
        )

        self.options_frame.pack(pady=10)

        self.option_var = tk.StringVar()

        self.option_buttons = []

        # BUTTON FRAME
        button_frame = tk.Frame(root, bg="#121212")
        button_frame.pack(pady=20)

        self.submit_button = tk.Button(
            button_frame,
            text="✅ Submit Answer",
            command=self.check_answer,
            font=("Arial", 15, "bold"),
            bg="#43a047",
            fg="white",
            width=20,
            height=2,
            bd=5,
            cursor="hand2"
        )

        self.submit_button.pack()

        # NEXT LEVEL BUTTON
        self.next_level_button = tk.Button(
            root,
            text="➡ NEXT LEVEL",
            command=self.next_level,
            font=("Arial", 16, "bold"),
            bg="#ff9800",
            fg="white",
            width=20,
            height=2,
            bd=5,
            cursor="hand2"
        )

        # TRY AGAIN BUTTON
        self.try_again_button = tk.Button(
            root,
            text="🔁 TRY AGAIN",
            command=self.try_again,
            font=("Arial", 16, "bold"),
            bg="#8e24aa",
            fg="white",
            width=20,
            height=2,
            bd=5,
            cursor="hand2"
        )

        # RESTART BUTTON
        self.restart_button = tk.Button(
            root,
            text="🔄 RESTART GAME",
            command=self.restart_game,
            font=("Arial", 16, "bold"),
            bg="#e53935",
            fg="white",
            width=20,
            height=2,
            bd=5,
            cursor="hand2"
        )

        self.load_question()

    # SETUP QUESTIONS
    def setup_questions(self):

        levels = {

            1: [
                ("What does CPU stand for?", ["Central Processing Unit", "Computer Power Unit", "Central Program Utility", "Control Processing Unit"], "Central Processing Unit"),
                ("What does RAM stand for?", ["Random Access Memory", "Read Access Memory", "Rapid Action Monitor", "Run Active Memory"], "Random Access Memory"),
                ("Which company made Windows?", ["Microsoft", "Apple", "Google", "IBM"], "Microsoft"),
                ("Which language is used for websites?", ["JavaScript", "Python", "C++", "Java"], "JavaScript"),
                ("Which is a web browser?", ["Chrome", "Excel", "Windows", "Python"], "Chrome"),
                ("Which key deletes text to the left?", ["Backspace", "Delete", "Shift", "Enter"], "Backspace"),
                ("What prints output in Python?", ["print()", "show()", "echo()", "display()"], "print()"),
                ("1 byte equals how many bits?", ["8", "4", "16", "32"], "8"),
                ("What does HTML stand for?", ["HyperText Markup Language", "Home Tool Markup Language", "Hyper Tool Machine Language", "Hyperlink Text Machine Language"], "HyperText Markup Language"),
                ("Which device moves the cursor?", ["Mouse", "Keyboard", "Printer", "Monitor"], "Mouse"),
                ("Shortcut for copy?", ["Ctrl+C", "Ctrl+V", "Ctrl+X", "Ctrl+A"], "Ctrl+C"),
                ("Shortcut for paste?", ["Ctrl+V", "Ctrl+C", "Ctrl+P", "Ctrl+X"], "Ctrl+V"),
                ("Which company created the iPhone?", ["Apple", "Samsung", "Nokia", "Sony"], "Apple"),
                ("What does WWW stand for?", ["World Wide Web", "Wide World Web", "World Web Window", "Web World Wide"], "World Wide Web"),
                ("Which is NOT a programming language?", ["HTML", "Python", "Java", "C++"], "HTML"),
                ("Which stores files permanently?", ["Hard Drive", "RAM", "CPU", "Cache"], "Hard Drive"),
                ("Which is an operating system?", ["Linux", "Python", "Excel", "HTML"], "Linux"),
                ("Which symbol is used for comments in Python?", ["#", "//", "/*", "--"], "#"),
                ("What does USB stand for?", ["Universal Serial Bus", "United System Bus", "User System Board", "Universal System Base"], "Universal Serial Bus"),
                ("What is the brain of the computer?", ["CPU", "RAM", "SSD", "GPU"], "CPU")
            ],

            2: [
                ("What does OOP stand for?", ["Object-Oriented Programming", "Open Output Process", "Optimal Object Program", "Operation Output Programming"], "Object-Oriented Programming"),
                ("Which keyword creates a function in Python?", ["def", "func", "function", "create"], "def"),
                ("Which data type stores True or False?", ["Boolean", "String", "Integer", "Float"], "Boolean"),
                ("Which loop repeats while a condition is true?", ["while", "for", "repeat", "loop"], "while"),
                ("What symbol is used for assignment in Python?", ["=", "==", ":", "!="], "="),
                ("Which operator checks equality?", ["==", "=", "!=", "<>"], "=="),
                ("Which collection uses key-value pairs?", ["Dictionary", "List", "Tuple", "Set"], "Dictionary"),
                ("Which method adds an item to a list?", ["append()", "add()", "insert()", "push()"], "append()"),
                ("What is the output type of input() in Python?", ["String", "Integer", "Boolean", "Float"], "String"),
                ("Which keyword exits a loop?", ["break", "stop", "exit", "return"], "break"),
                ("Which keyword skips one loop iteration?", ["continue", "skip", "pass", "next"], "continue"),
                ("What symbol starts a Python decorator?", ["@", "#", "&", "$"], "@"),
                ("Which function returns list length?", ["len()", "size()", "count()", "length()"], "len()"),
                ("Which keyword defines a class?", ["class", "object", "define", "struct"], "class"),
                ("What is inheritance in OOP?", ["Reusing class features", "Deleting classes", "Copying variables", "Creating loops"], "Reusing class features"),
                ("Which statement handles exceptions?", ["try", "catch", "throw", "attempt"], "try"),
                ("What is the correct extension for Python files?", [".py", ".python", ".pt", ".p"], ".py"),
                ("Which statement is used to import modules?", ["import", "include", "using", "require"], "import"),
                ("Which operator means 'not equal'?", ["!=", "<>", "==", "="], "!="),
                ("Which function converts text to integer?", ["int()", "str()", "float()", "bool()"], "int()")
            ],

            3: [
                ("Which sorting algorithm is fastest on average?", ["Quick Sort", "Bubble Sort", "Selection Sort", "Insertion Sort"], "Quick Sort"),
                ("What data structure uses FIFO?", ["Queue", "Stack", "Tree", "Graph"], "Queue"),
                ("What data structure uses LIFO?", ["Stack", "Queue", "Heap", "Array"], "Stack"),
                ("Which algorithm finds shortest path?", ["Dijkstra", "Bubble Sort", "DFS", "Merge Sort"], "Dijkstra"),
                ("Which search has O(log n) complexity?", ["Binary Search", "Linear Search", "DFS", "BFS"], "Binary Search"),
                ("Which traversal uses recursion naturally?", ["DFS", "BFS", "Linear", "Circular"], "DFS"),
                ("Which structure stores nodes hierarchically?", ["Tree", "Queue", "Stack", "Array"], "Tree"),
                ("Which database language is standard?", ["SQL", "HTML", "CSS", "XML"], "SQL"),
                ("What does API stand for?", ["Application Programming Interface", "Applied Program Internet", "Application Process Integration", "Advanced Programming Interface"], "Application Programming Interface"),
                ("Which protocol secures websites?", ["HTTPS", "HTTP", "FTP", "SMTP"], "HTTPS"),
                ("What does IDE stand for?", ["Integrated Development Environment", "Internal Design Engine", "Integrated Device Execution", "Internet Development Editor"], "Integrated Development Environment"),
                ("Which company developed Java?", ["Sun Microsystems", "Microsoft", "Google", "IBM"], "Sun Microsystems"),
                ("Which command initializes Git?", ["git init", "git start", "git create", "git begin"], "git init"),
                ("Which Git command uploads commits?", ["git push", "git pull", "git upload", "git commit"], "git push"),
                ("Which Git command downloads changes?", ["git pull", "git push", "git fetch", "git commit"], "git pull"),
                ("What does SQL stand for?", ["Structured Query Language", "System Query Language", "Sequential Query Logic", "Structured Question Language"], "Structured Query Language"),
                ("Which normal form removes partial dependency?", ["2NF", "1NF", "3NF", "BCNF"], "2NF"),
                ("Which HTTP method retrieves data?", ["GET", "POST", "PUT", "DELETE"], "GET"),
                ("Which HTTP method sends data?", ["POST", "GET", "TRACE", "HEAD"], "POST"),
                ("Which database is NoSQL?", ["MongoDB", "MySQL", "PostgreSQL", "Oracle"], "MongoDB")
            ],

            4: [
                ("Which principle says a class should have one responsibility?", ["Single Responsibility Principle", "Open Closed Principle", "Dependency Inversion", "Liskov Substitution"], "Single Responsibility Principle"),
                ("Which design pattern creates one object only?", ["Singleton", "Factory", "Observer", "Builder"], "Singleton"),
                ("Which principle allows extension without modification?", ["Open Closed Principle", "Single Responsibility", "Encapsulation", "Abstraction"], "Open Closed Principle"),
                ("Which algorithm uses divide and conquer?", ["Merge Sort", "Bubble Sort", "Selection Sort", "Linear Search"], "Merge Sort"),
                ("Which structure uses hashing?", ["Hash Table", "Queue", "Tree", "Graph"], "Hash Table"),
                ("Which complexity is better?", ["O(log n)", "O(n²)", "O(n³)", "O(2ⁿ)"], "O(log n)"),
                ("What does JVM stand for?", ["Java Virtual Machine", "Java Variable Method", "Joint Virtual Method", "Java Verified Machine"], "Java Virtual Machine"),
                ("Which language is mainly used for Android?", ["Kotlin", "Swift", "Ruby", "PHP"], "Kotlin"),
                ("Which language is mainly used for iOS?", ["Swift", "Kotlin", "Python", "Java"], "Swift"),
                ("Which protocol transfers files?", ["FTP", "SMTP", "HTTP", "TCP"], "FTP"),
                ("Which protocol sends emails?", ["SMTP", "FTP", "SSH", "POP"], "SMTP"),
                ("What does CSS stand for?", ["Cascading Style Sheets", "Creative Style System", "Computer Style Sheets", "Colorful Style Syntax"], "Cascading Style Sheets"),
                ("Which tag creates a hyperlink in HTML?", ["<a>", "<p>", "<h1>", "<img>"], "<a>"),
                ("Which company developed Python?", ["Python Software Foundation", "Microsoft", "Apple", "Google"], "Python Software Foundation"),
                ("Which database relation is many-to-many?", ["Students and Subjects", "Country and Capital", "Person and Passport", "User and Username"], "Students and Subjects"),
                ("What does DNS stand for?", ["Domain Name System", "Data Network Service", "Digital Number System", "Direct Name Server"], "Domain Name System"),
                ("Which port does HTTP use by default?", ["80", "21", "25", "443"], "80"),
                ("Which port does HTTPS use?", ["443", "80", "21", "22"], "443"),
                ("Which company developed C language?", ["Bell Labs", "Google", "IBM", "Apple"], "Bell Labs"),
                ("Which language is best known for AI?", ["Python", "HTML", "CSS", "PHP"], "Python")
            ],

            5: [
                ("Which algorithm is used in blockchain mining?", ["SHA-256", "RSA", "AES", "DES"], "SHA-256"),
                ("What does AI stand for?", ["Artificial Intelligence", "Automated Internet", "Applied Interface", "Artificial Integration"], "Artificial Intelligence"),
                ("Which AI model learns from labeled data?", ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Deep Search"], "Supervised Learning"),
                ("Which network device routes traffic?", ["Router", "Switch", "Hub", "Repeater"], "Router"),
                ("Which cybersecurity attack overloads servers?", ["DDoS", "Phishing", "Spoofing", "Sniffing"], "DDoS"),
                ("Which encryption is symmetric?", ["AES", "RSA", "ECC", "DES"], "AES"),
                ("Which encryption is asymmetric?", ["RSA", "AES", "DES", "Blowfish"], "RSA"),
                ("What does VPN stand for?", ["Virtual Private Network", "Verified Personal Network", "Virtual Process Node", "Visual Private Net"], "Virtual Private Network"),
                ("Which OS is open-source?", ["Linux", "Windows", "macOS", "iOS"], "Linux"),
                ("Which layer handles routing in OSI?", ["Network Layer", "Transport Layer", "Session Layer", "Physical Layer"], "Network Layer"),
                ("Which layer handles encryption in OSI?", ["Presentation Layer", "Network Layer", "Transport Layer", "Application Layer"], "Presentation Layer"),
                ("What does TCP stand for?", ["Transmission Control Protocol", "Transfer Communication Protocol", "Transport Control Process", "Transmission Core Protocol"], "Transmission Control Protocol"),
                ("Which protocol is connectionless?", ["UDP", "TCP", "HTTP", "FTP"], "UDP"),
                ("What does LAN stand for?", ["Local Area Network", "Large Access Network", "Local Access Node", "Linked Area Network"], "Local Area Network"),
                ("What does WAN stand for?", ["Wide Area Network", "Wireless Area Network", "Wide Access Node", "Web Area Network"], "Wide Area Network"),
                ("Which language is used for machine learning most?", ["Python", "C#", "PHP", "HTML"], "Python"),
                ("Which company developed TensorFlow?", ["Google", "Microsoft", "IBM", "Amazon"], "Google"),
                ("Which database is graph-based?", ["Neo4j", "MySQL", "MongoDB", "SQLite"], "Neo4j"),
                ("Which Linux command lists files?", ["ls", "dir", "list", "show"], "ls"),
                ("Which Linux command changes directory?", ["cd", "mv", "ls", "mkdir"], "cd")
            ]
        }

        for level, questions in levels.items():

            for q in questions:
                self.question_bank.add_question(
                    level,
                    q[0],
                    q[1],
                    q[2]
                )

    # LOAD QUESTION
    def load_question(self):

        try:

            self.current_question = self.question_bank.get_random_question(
                self.current_level
            )

            self.question_label.config(
                text=self.current_question["question"],
                fg="white"
            )

            self.option_var.set("")

            for btn in self.option_buttons:
                btn.destroy()

            self.option_buttons.clear()

            # RANDOMIZE ANSWERS
            options = self.current_question["options"].copy()
            random.shuffle(options)

            for option in options:

                btn = tk.Radiobutton(
                    self.options_frame,
                    text=option,
                    variable=self.option_var,
                    value=option,
                    font=("Arial", 15, "bold"),
                    bg="#1e1e1e",
                    fg="white",
                    activebackground="#42a5f5",
                    activeforeground="white",
                    selectcolor="#43a047",
                    width=45,
                    height=2,
                    indicatoron=False,
                    relief="raised",
                    bd=4,
                    cursor="hand2"
                )

                btn.pack(pady=8)

                self.option_buttons.append(btn)

        except ValueError:
            self.game_over()

    # CHECK ANSWER
    def check_answer(self):

        user_answer = self.option_var.get()

        if user_answer == "":
            messagebox.showwarning(
                "Warning",
                "Please select an answer!"
            )
            return

        self.questions_answered += 1

        if user_answer == self.current_question["answer"]:

            self.player.correct_answer()
            self.robot.wrong_answer()

            messagebox.showinfo(
                "Correct!",
                "✅ Correct Answer!"
            )

        else:

            self.player.wrong_answer()

            messagebox.showerror(
                "Wrong!",
                f"❌ Wrong Answer!\n\nCorrect Answer:\n{self.current_question['answer']}"
            )

        self.player_label.config(
            text=self.player.get_stats()
        )

        self.robot_label.config(
            text=self.robot.get_stats()
        )

        self.counter_label.config(
            text=f"LEVEL {self.current_level} | Questions: {self.questions_answered}/20"
        )

        # PLAYER LOSE
        if self.player.health <= 0:
            self.game_over()
            return

        # ROBOT LOSE
        if self.robot.health <= 0:

            for btn in self.option_buttons:
                btn.destroy()

            self.option_buttons.clear()

            self.submit_button.pack_forget()

            if self.current_level < 5:

                self.question_label.config(
                    text=f"🏆 LEVEL {self.current_level} COMPLETE!\nBOT DEFEATED!",
                    fg="#76ff03"
                )

                self.next_level_button.place(
                    relx=0.5,
                    rely=0.75,
                    anchor="center"
                )

            else:

                self.question_label.config(
                    text="🏆 FINAL VICTORY!\nYOU BEAT ALL LEVELS!",
                    fg="#76ff03"
                )

                self.restart_button.place(
                    relx=0.5,
                    rely=0.75,
                    anchor="center"
                )

            return

        # AUTO NEXT QUESTION
        self.root.after(300, self.load_question)

    # NEXT LEVEL
    def next_level(self):

        self.current_level += 1

        self.questions_answered = 0

        self.robot = PlayerStats("🤖 Robot Enemy")

        self.robot_label.config(
            text=self.robot.get_stats()
        )

        self.counter_label.config(
            text=f"LEVEL {self.current_level} | Questions: 0/20"
        )

        self.next_level_button.place_forget()

        self.submit_button.pack()

        self.load_question()

    # GAME OVER
    def game_over(self):

        for btn in self.option_buttons:
            btn.destroy()

        self.option_buttons.clear()

        self.submit_button.pack_forget()

        self.question_label.config(
            text=f"💀 GAME OVER\nYOU LOST IN LEVEL {self.current_level}!",
            fg="red"
        )

        # TRY AGAIN BUTTON
        self.try_again_button.place(
            relx=0.40,
            rely=0.78,
            anchor="center"
        )

        # RESTART BUTTON
        self.restart_button.place(
            relx=0.60,
            rely=0.78,
            anchor="center"
        )

    # TRY AGAIN
    def try_again(self):

        # RESET PLAYER
        self.player = PlayerStats(self.player.name)

        # RESET ROBOT
        self.robot = PlayerStats("🤖 Robot Enemy")

        # RESET QUESTION COUNT
        self.questions_answered = 0

        # RESET QUESTION BANK
        self.question_bank = QuestionBank()
        self.setup_questions()

        self.player_label.config(
            text=self.player.get_stats()
        )

        self.robot_label.config(
            text=self.robot.get_stats()
        )

        self.counter_label.config(
            text=f"LEVEL {self.current_level} | Questions: 0/20"
        )

        self.restart_button.place_forget()
        self.try_again_button.place_forget()
        self.next_level_button.place_forget()

        self.submit_button.pack()

        self.load_question()

    # RESTART GAME
    def restart_game(self):

        self.current_level = 1

        self.player = PlayerStats(self.player.name)
        self.robot = PlayerStats("🤖 Robot Enemy")

        self.questions_answered = 0

        self.question_bank = QuestionBank()
        self.setup_questions()

        self.player_label.config(
            text=self.player.get_stats()
        )

        self.robot_label.config(
            text=self.robot.get_stats()
        )

        self.counter_label.config(
            text="LEVEL 1 | Questions: 0/20"
        )

        self.restart_button.place_forget()
        self.try_again_button.place_forget()
        self.next_level_button.place_forget()

        self.submit_button.pack()

        self.load_question()


# START SCREEN
if __name__ == "__main__":

    root = tk.Tk()

    root.title("⚔ Battle Simulator")
    root.geometry("450x320")
    root.configure(bg="#121212")

    title = tk.Label(
        root,
        text="⚔ BATTLE SIMULATOR ⚔",
        font=("Arial", 24, "bold"),
        fg="#ffca28",
        bg="#121212"
    )

    title.pack(pady=20)

    label = tk.Label(
        root,
        text="Enter Your Name",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#121212"
    )

    label.pack(pady=10)

    name_entry = tk.Entry(
        root,
        font=("Arial", 16),
        width=20,
        justify="center",
        bg="#1e1e1e",
        fg="white",
        insertbackground="white"
    )

    name_entry.pack(pady=15)

    def start_game():

        player_name = name_entry.get().strip()

        if player_name == "":

            messagebox.showwarning(
                "Warning",
                "Please enter your name!"
            )

            return

        root.destroy()

        game_root = tk.Tk()

        App(game_root, player_name)

        game_root.mainloop()

    start_button = tk.Button(
        root,
        text="🚀 START GAME",
        command=start_game,
        font=("Arial", 16, "bold"),
        bg="#1e88e5",
        fg="white",
        width=15,
        height=2,
        bd=5,
        cursor="hand2"
    )

    start_button.pack(pady=20)

    root.mainloop()