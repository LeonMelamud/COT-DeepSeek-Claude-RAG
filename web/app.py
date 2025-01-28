from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from rat.rat import ModelChain as OpenRouterChain
import importlib.util
import sys
import json

# Import rat-claude.py dynamically
spec = importlib.util.spec_from_file_location("rat_claude", "rat-claude.py")
rat_claude = importlib.util.module_from_spec(spec)
sys.modules["rat_claude"] = rat_claude
spec.loader.exec_module(rat_claude)
ClaudeChain = rat_claude.ModelChain

app = Flask(__name__)
load_dotenv()

# Initialize both chains with error handling
openrouter_chain = None
claude_chain = None

try:
    openrouter_chain = OpenRouterChain()
except ValueError as e:
    print(f"Error initializing OpenRouter chain: {e}")

try:
    claude_chain = ClaudeChain()
except ValueError as e:
    print(f"Error initializing Claude chain: {e}")

@app.route('/')
def index():
    return render_template('index.html', result={})

def validate_key(key_name):
    key = os.getenv(key_name, '')
    # Always load fresh from env file
    load_dotenv()
    return bool(key and key.strip() and key != f'your_{key_name.lower()}_here')

@app.route('/api/env', methods=['GET'])
def get_env():
    return jsonify({
        'DEEPSEEK_API_KEY': {'isValid': validate_key('DEEPSEEK_API_KEY')},
        'OPENROUTER_API_KEY': {'isValid': validate_key('OPENROUTER_API_KEY')},
        'ANTHROPIC_API_KEY': {'isValid': validate_key('ANTHROPIC_API_KEY')}
    })

@app.route('/api/env', methods=['POST'])
def update_env():
    data = request.json
    env_content = []
    
    for key, value in data.items():
        if value:  # Only add non-empty values
            env_content.append(f'{key}={value}')
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write('\n'.join(env_content))
    
    load_dotenv()  # Reload environment variables
    return jsonify({'status': 'success'})

@app.route('/api/rag', methods=['POST'])
def process_rag():
    mode = request.args.get('mode', 'openrouter')
    chain = openrouter_chain if mode == 'openrouter' else claude_chain
    
    if not chain:
        return jsonify({'error': f'API keys not properly configured for {mode} mode. Please check your environment variables.'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save file temporarily
    temp_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(temp_path)
    
    try:
        # Read file content
        with open(temp_path, 'r') as f:
            content = f.read()
        
        # Get reasoning from DeepSeek
        reasoning = chain.get_deepseek_reasoning(f"Analyze this content: {content}")
        
        # Get response based on mode
        if mode == 'openrouter':
            response = chain.get_openrouter_response(f"Analyze this content: {content}", reasoning)
        else:
            response = chain.get_claude_response(f"Analyze this content: {content}", reasoning)
        
        return jsonify({
            'reasoning': reasoning,
            'response': response
        })
    finally:
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == '__main__':
    app.run(debug=True)
