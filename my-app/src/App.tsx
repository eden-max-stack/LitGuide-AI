import React, { useState, useEffect, useRef, ChangeEvent, KeyboardEvent } from 'react';
import { useQuery, useMutation } from "convex/react";
import { api } from "../convex/_generated/api";
import './App.css'; // Import your styles

// Define the structure of a message
interface Message {
  _id: string;
  body: string;
  author: string;
}

const App: React.FC = () => {
  // State to store chat messages
  const [messages, setMessages] = useState<Message[]>([]);
  
  // State to store the current message input
  const [newMessageText, setNewMessageText] = useState<string>('');

  // State to store the PDF file
  const [pdfFiles, setPdfFiles] = useState<File[]>([]); // Correctly initialized as an array
  
  // Reference to chat box for scrolling
  const chatBoxRef = useRef<HTMLDivElement>(null);

  // Flags for each PDF option
  const [isChatWithPdf, setIsChatWithPdf] = useState<boolean>(false);
  const [isSummarizePdf, setIsSummarizePdf] = useState<boolean>(false);
  const [isFetchPapers, setIsFetchPapers] = useState<boolean>(false);
  const [isTechStackRec, setIsTechStackRec] = useState<boolean>(false);

  // Hook to fetch messages from Convex (if needed)
  //const fetchedMessages = useQuery(api.messages.listMessages); // Uncomment if you want to fetch messages on load
  const sendMessage = useMutation(api.messages.send);

  const renderMessageContent = (message: Message): JSX.Element => {
    try {
      if (message.author === 'Gemini' && isFetchPapers) {
        // Parse the AI's response
        const data = message.body;
        console.log(data);
  
        if (
          Array.isArray(data) &&
          typeof data[0] === 'string' && // Check that the first element is a string (the topic)
          Array.isArray(data[1]) && data[1].every((item) => typeof item === 'string') && // Check that the second element is an array of strings (titles)
          Array.isArray(data[2]) && data[2].every((item) => typeof item === 'string') // Check that the third element is an array of strings (URLs)
        ) {
        const topic = data[0]; // First element is the topic
        const titles: string[] = data[1]; // Second element is the list of titles
        const links: string[] = data[2]; // Third element is the list of URLs
  
        return (
          <>
            <h3>{topic}</h3> {/* Render the topic */}
            <ol>
              {titles.map((title, index) => (
                <li key={index}>
                  <a href={links[index]} target="_blank" rel="noopener noreferrer">
                    {title}
                  </a>
                </li>
              ))}
            </ol>
          </>
        );
      } else {
        // If data structure isn't as expected, render a fallback message
        return <p>Unexpected AI response format.</p>;
      } }
      else if (message.author === 'Gemini' && isTechStackRec) {
        const data = message.body;
        console.log(data);
    
        // Check that data is an array and contains the correct structure
        if (
            Array.isArray(data) &&
            data.every((item) => Array.isArray(item) && item.length === 2) // Each item should be an array with 2 elements
        ) {
            // Create an array of React elements
            const output = data.map(([techStack, popularity]) => {
                return (
                    <div key={techStack}> {/* Ensure a unique key for each item */}
                        {techStack} : {popularity}
                    </div>
                );
            });
    
            return <>{output}</>; // Wrap in a fragment and return
        }
    }
    
      else {
        // For user messages, just render the text
        return <p>{message.body}</p>;
      }
    } catch (error) {
      console.error("Error parsing AI response:", error);
      return <p>{message.body}</p>; // Fallback in case of a parsing error
    }
  };  
  
  /*const downloadPDF = async(e: React.FormEvent) => {
    e.preventDefault();

    // Send the message to the Python backend
    try {
      const response = await fetch('', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt: newMessageText }),
      });

      const data = await response.json();
      console.log('Response from Python:', data.response);
    } catch (error) {
      console.error('Error sending prompt to Python:', error);
    }

    // Clear input field
    setNewMessageText('');
  }; */

  // Handle Fetch Papers
  const handleFetchPapers = (e: React.FormEvent) => {
    e.preventDefault();
    setIsFetchPapers(true); // Set the flag for fetch papers
    setIsChatWithPdf(false);  // Reset other flags
    setIsSummarizePdf(false);
    setIsTechStackRec(false);

    handleSendMessage(e); // Send the message for fetching papers
  };

  // Handle PDF file selection
  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      // Convert the FileList to an array and set it to state
      const selectedFiles = Array.from(e.target.files);
      setPdfFiles(selectedFiles);
    }
  };

  // Handle Summarize PDF
  const handleSummarizePDF = async () => {
    setIsSummarizePdf(true); // Set the flag for summarize PDF
    setIsChatWithPdf(false);  // Reset other flags
    setIsFetchPapers(false);
    setIsTechStackRec(false);


  // Prepare the FormData for the PDF files
  const formData = new FormData();
  pdfFiles.forEach((file) => {
    formData.append("file", file); // Send multiple files in one form
  });

  // Step 1: Add the user's prompt to the chat
  const userMessageId = Date.now().toString();
  const userMessage: Message = {
    _id: userMessageId,
    body: 'Provide a summary on the uploaded file, please!',
    author: 'User',
  };

  setMessages((prevMessages) => [...prevMessages, userMessage]);  

  try {
    const response = await fetch("http://localhost:8080/api/summarize-pdf", {
        method: "POST",
        body: formData, // Ensure you're sending FormData, not JSON
      });

      const data = await response.json();

      if (response.ok && data.response) {
        console.log("Response from Python:", data.response);

        // AI's summary response
        const aiResponseId = Date.now() + 1;
        const aiResponse: Message = {
          _id: aiResponseId.toString(),
          body: data.response,
          author: 'Gemini',
        };

        // Add the AI's summary to the messages
        setMessages((prevMessages) => [...prevMessages, aiResponse]);

        // Send the message to Convex (if needed)
        try {
          await sendMessage({ author: 'Gemini', message: data.response });
        } catch (error) {
          console.error('Error saving summary to Convex:', error);
        }
      } else {
        console.error("Error from server:", data.error);
      }
    } catch (error) {
      console.error("Error summarizing PDF:", error);
    }

    // Clear input field
    setNewMessageText('');

  };

  const handleChatWithPDF = async () => {
    setIsChatWithPdf(true); // Set the flag for chat with PDF
    setIsSummarizePdf(false); // Reset other flags
    setIsFetchPapers(false);
    setIsTechStackRec(false);

    if (!pdfFiles || pdfFiles.length === 0) {
      alert("Please upload at least one PDF file.");
      return;
    }

    // Step 1: Add the user's prompt to the chat
    const userMessageId = Date.now().toString();
    const userMessage: Message = {
      _id: userMessageId,
      body: newMessageText,
      author: 'User',
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
  
    const formData = new FormData();
    pdfFiles.forEach((file) => {
      formData.append("file", file); // Make sure this matches the key in Flask
    });
    
    // If there's a prompt, append it to the FormData
    formData.append("question", newMessageText); 
  
    try {
      const response = await fetch("http://localhost:8080/api/chat-with-pdf", {
        method: "POST",
        body: formData, // Ensure body contains formData
      });
  
      const data = await response.json();
  
      if (response.ok) {
        console.log("Response from Python:", data.response);
        
        // AI response
        if (data.response) { // Check if response is defined
          const aiResponseId = Date.now() + 1;
          const aiResponse: Message = {
            _id: aiResponseId.toString(),
            body: data.response,
            author: 'Gemini', // AI's author
          };

          // Add AI's response to the message list
          setMessages((prevMessages) => [...prevMessages, aiResponse]);

          try {
            await sendMessage({ author : 'Gemini', message : data.response});
          } catch (error) {
            console.error(error);
          }
      } else {
        console.error("Error from server:", data.error);
      }
    }
   } catch (error) {
      console.error("Error chatting with PDF:", error);
    }
  };
  
  
  // Function to handle sending a message and generating an AI response
const handleSendMessage = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!newMessageText.trim()) {
    alert("Message cannot be empty.");
    return;
  }

  // Create a unique ID for the user message
  const userMessageId = Date.now().toString();

  // User's message
  const userMessage: Message = {
    _id: userMessageId,
    body: newMessageText,
    author: 'User',
  };

  // Add user's message to the message list
  setMessages((prevMessages) => [...prevMessages, userMessage]);

  // Send the message to Convex
  try {
    await sendMessage({ message: newMessageText, author: 'User' });
  } catch (error) {
    console.error('Error sending user message to Convex:', error);
  }

  // Send the message to the Python backend
  try {
    const response = await fetch('http://localhost:8080/api/send-prompt', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: newMessageText }),
      mode: 'cors'
    });

    const data = await response.json();
    console.log('Response from Python:', data.response);

    // AI response
    if (data.response) { // Check if response is defined
      const aiResponseId = Date.now() + 1; 
      const aiResponse: Message = {
        _id: aiResponseId.toString(),
        body: data.response,
        author: 'Gemini',
      };

      // Add AI's response to the message list
      setMessages((prevMessages) => [...prevMessages, aiResponse]);

      // Save AI response to the database
      try {
        await sendMessage({ author: 'ai', message: aiResponse.body }); // Ensure `data.response` is defined
      } catch (error) {
        console.error('Error sending AI message to Convex:', error);
      }
    } else {
      console.error('Error: No response from Python.');
    }
  } catch (error) {
    console.error('Error sending prompt to Python:', error);
  }

  // Clear input field
  setNewMessageText('');
};

const handleTechStackRec = async () => {
  setIsChatWithPdf(false); // Set the flag for chat with PDF
  setIsSummarizePdf(false); // Reset other flags
  setIsFetchPapers(false);
  setIsTechStackRec(true);

  if (!newMessageText.trim()) {
    alert("Message cannot be empty.");
    return;
  }

  // Create a unique ID for the user message
  const userMessageId = Date.now().toString();

  // User's message
  const userMessage: Message = {
    _id: userMessageId,
    body: newMessageText,
    author: 'User',
  };

  // Add user's message to the message list
  setMessages((prevMessages) => [...prevMessages, userMessage]);

  // Send the message to Convex
  try {
    await sendMessage({ message: newMessageText, author: 'User' });
  } catch (error) {
    console.error('Error sending user message to Convex:', error);
  }

  try {
    const response = await fetch('http://localhost:8080/api/recommend-ts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt: newMessageText }),
    });

    const data = await response.json();
    console.log("Response from Python: ", data.response);

    if (data.response) {
      const aiResponseId = Date.now() + 1;
      const aiResponse: Message = {
        _id: aiResponseId.toString(),
        body: data.response,
        author: 'Gemini',
      };

      setMessages((prevMessages) => [...prevMessages, aiResponse]);

      try {
        await sendMessage({ author: 'ai', message: aiResponse.body }); // Ensure `data.response` is defined
      } catch (error) {
        console.error('Error sending AI message to Convex:', error);
      }
    } else {
      console.error('Error: No response from Python.');
    }
  } catch (error) {
    console.error('Error sending prompt to Python:', error);
  }

  // Clear input field
  setNewMessageText('');
};

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    if (chatBoxRef.current) {
      chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
    }
  }, [messages]);

  // Handle input change
  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    setNewMessageText(e.target.value);
  };

  return (
    <div className="container">
      {/* Left Panel */}
      <div className="left-panel">
        <h3>Upload PDF</h3>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
      </div>
      
      {/* Right Panel */}
      <div className="right-panel">
        {/* Chat Box */}
        <div className="chat-box" ref={chatBoxRef}>
        {messages.map((message) => (
            <article
            key={message._id}
            className={`message ${message.author === 'User' ? "user-message" : "ai-response"}`}
          >
            <div>{message.author}</div>
            {renderMessageContent(message)}
          </article>
  ))}
</div>

        {/* Centered Buttons */}
        <div className="pdf-options">
          <button onClick={(handleChatWithPDF)}>Chat with PDF</button>
          <button onClick={(handleSummarizePDF)}>Summarize PDF</button>
          <button onClick={handleFetchPapers} disabled={!newMessageText}>Fetch Papers</button>
          <button onClick={(handleTechStackRec)}>Recommend Tech Stack</button>
        </div>
        
        {/* Input Area */}
        <div className="input-area">
          <form onSubmit={handleSendMessage}>
            <input
              type="text"
              placeholder="Type your message..."
              value={newMessageText}
              onChange={handleInputChange} 
            />
            <button type="submit" className="hidden" disabled={!newMessageText}>Send</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default App;
