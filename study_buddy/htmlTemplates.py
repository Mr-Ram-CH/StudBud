css = '''
<style>
/* General Styles */
body {
    font-family: 'Arial', sans-serif;
    background-color: #f4f4f9;
    color: #333;
}

/* Chat Message Styles */
.chat-message {
    padding: 1.5rem;
    border-radius: 1rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chat-message:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.chat-message.user {
    background-color: #2b313e;
    color: #fff;
}

.chat-message.bot {
    background-color: #475063;
    color: #fff;
}

.chat-message .avatar {
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
    animation: float 3s ease-in-out infinite;
}

.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    font-size: 1rem;
    line-height: 1.5;
}

/* Study Planner Styles */
.study-plan {
    background-color: #ffffff;
    padding: 1rem;
    border-radius: 1rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.study-plan:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.study-plan h3 {
    color: #2b313e;
    margin-bottom: 0.5rem;
    font-size: 1.5rem;
    font-weight: bold;
}

.study-plan .plan-content {
    color: #475063;
    font-size: 1rem;
    line-height: 1;
    white-space: pre-wrap; /* Preserve formatting for study plan text */
}

/* Animations */
@keyframes float {
    0%, 100% {
        transform: translateY(0);
    }
    50% {
        transform: translateY(-10px);
    }
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.pinimg.com/originals/79/04/42/7904424933cc535b666f2de669973530.gif" 
        style="max-height: 100px; max-width: 100px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://cdnl.iconscout.com/lottie/premium/thumb/student-7543029-6111861.gif">
    </div>      
    <div class="message">{{MSG}}</div>
</div>
'''

study_plan_template = '''
<div class="study-plan">
    <h3>Your Study Plan</h3>
    <div class="plan-content">
        {{STUDY_PLAN}}
    </div>
</div>
'''