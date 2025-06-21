# digitest.llm - ATPG Test Vector Generation Tool

## Overview

`digitest.llm` is an interactive tool for Automatic Test Pattern Generation (ATPG) using a fine-tuned Llama-2-7b-chat model. It analyzes structural Verilog netlists to generate test vectors for detecting stuck-at faults.

### Research Goal
The objective is not to replace existing ATPG workflows, but to explore how a specialized LLM can autonomously perform test generation as a language-based reasoning task. We aim to uncover new opportunities for adaptability and automation in ATPG.

> **Note**: The model's performance is sensitive to how the user prompt is structured. Feedback for improving its robustness is highly appreciated!

## Features

- **Interactive Prompt Interface**: Chat-like interface for entering circuit descriptions and test requirements
- **Fine-tuned Model**: Uses a specialized Llama-2-7b-chat model trained for ATPG tasks
- **Structured Output**: Generates test vectors with simulation results, input vectors, expected outputs, and detected faults
- **Real-time Streaming**: Provides real-time text generation with streaming output
- **Memory Management**: Efficient GPU memory management with automatic cleanup

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd digitest.llm
```

### 2. Install Dependencies
```bash
# Or install core dependencies manually
pip install torch==2.5.1 transformers==4.49.0 peft==0.13.2
```

### 3. Model Access Setup
The tool uses the following models:
- **Base Model**: `meta-llama/Llama-2-7b-chat-hf` (requires Hugging Face access)
- **Fine-tuned Model**: `chrivasileiou/digitest` (publicly available)

To access the base Llama-2 model, you need to:
1. Request access at [Hugging Face Llama-2](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)
2. Accept the license terms
3. Generate an access token at [Hugging Face Settings](https://huggingface.co/settings/tokens)
4. Login using: `huggingface-cli login`

## Configuration

### GPU Device Configuration
The script is configured to use CUDA device by default. To change this, modify the device line in `generate.py`:

```python
device = torch.device('cuda')  # Change to your preferred GPU
```

### Model Configuration
The script uses the following default configuration:
- **Base Model**: `meta-llama/Llama-2-7b-chat-hf`
- **Fine-tuned Model**: `chrivasileiou/digitest`
- **Adapter**: `grpo_adapter`
- **Precision**: bfloat16
- **Attention**: Flash Attention 2

## Usage

### Basic Usage
```bash
python generate.py
```

### Interactive Commands
Once the script is running, you can use the following commands:

- **Enter your prompt**: Type your instruction stuck-at fault target and netlist 
- **`example`**: Use the built-in example prompt for testing
- **`model`**: Print model information to terminal for verification
- **`exit` or `quit`**: Exit the program

### Example Session
```
Enter your prompt: example

[Model generates test vector for circuit_39868 with stuck-at fault sa0 _0007_]

Enter your prompt: model

[Model information is printed to terminal for verification]

Enter your prompt: Please generate a test vector for a 2-input AND gate with sa1 fault on the output

[Model generates appropriate test vector]

Enter your prompt: exit
```

## Input Format

### Circuit Description
Provide circuit descriptions in structural Verilog format:

```verilog
module circuit_name ( input1, input2, ..., output1, output2, ... );
    // Gate instantiations
    AND2 gate1 ( wire1, input1, input2 );
    OR2 gate2 ( output1, wire1, input3 );
endmodule
```

### Fault Specification
Specify faults using standard ATPG notation:
- **Stuck-at-0**: `sa0 <signal_name>`
- **Stuck-at-1**: `sa1 <signal_name>`

### Example Prompt
```
Please formulate a test vector for the circuit "circuit_39868" to address the "sa0 _0007_" based on this netlist:

module circuit_39868 ( _0000_,  _0001_,  _0002_,  _0003_, _0011_ );
    XNR2 _0004_ ( _0005_, _0001_, _0002_ );
    XOR2 _0006_ ( _0007_, _0000_, _0003_ );
    AN2 _0010_ ( _0011_, _0007_, _0005_ );
endmodule
```

## License

This project is licensed under the terms specified in the LICENSE file.
