import React, { useState, useEffect, useRef } from 'react'
import './static/css/chatInterface.css'

import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import MarkdownRenderer from './MarkdownRenderer';

import { PacmanLoader } from 'react-spinners';

import { BsArrowRightCircle } from "react-icons/bs"
import { FaUser } from "react-icons/fa";
import { RiRobot2Line } from "react-icons/ri";

import config from './config'

const ChatInterface = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [conversation, setConversation] = useState([]);
  const [currentInput, setCurrentInput] = useState("");
  const [numberOfInteractions, setNumberOfInteractions] = useState(0);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (messagesEndRef.current){
      messagesEndRef.current.scrollIntoView({
        behavior: "smooth"
      });
    }
  }, [conversation]);


  const clearChat = () => {
    const url = config.apiUrl + "/clear-chat";

    fetch(url)
    .then(resp => {
      if (!resp.ok){
        throw new Error("Failed clearing the chat!")
      }

      setConversation([]);
    })
  }


  const postQuery = () => {
    var conversation_cp = [];
    for (var i = 0; i < conversation.length; i++){
      conversation_cp.push(conversation[i]);
    }
    conversation_cp.push({
      user: currentInput,
      bot: null
    });
    setConversation(conversation_cp);

    // send the input to the backend using "fetch"
    setIsLoading(true);
    const url = config.apiUrl + "/ask-assistant";
    const data = {
      prompt: currentInput
    };

    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    };

    fetch(url, options)
    .then(response => {
      if (!response.ok){
        throw new Error("Response not ok!");
      }

      return response.json();
    })
    .then(data => {
      setConversation(data.conversation);
      console.log(data.conversation);
      setIsLoading(false);
    });

    // reset current input value
    setCurrentInput("");

    setNumberOfInteractions(numberOfInteractions + 1);
  }

  const sample_md = `
\`\`\`python
print("hello world")
\`\`\`
`;

  return (
    <div className='content'>
        <div className='conversation-wrapper'>
          <div>
            {conversation.map((el) => {
              const isLast = el == conversation[conversation.length - 1];

              return <div className='chat-row'>
                <div className='chat-el-user row'>
                  <div className='icon-span col-sm icon-col'>
                    <FaUser />
                  </div>
                  <div className='chat-text-span col-sm text-col'>
                    <MarkdownRenderer content={el.user}>
                    </MarkdownRenderer>
                    {/*
                    <Markdown remarkPlugins={[remarkGfm]}>
                      {el.user}
                    </Markdown>
                    */}
                  </div>
                </div>
                
                <div className='chat-el-bot row'>
                  {isLast && isLoading ?
                    <div className='icon-span col-sm icon-col'>
                      <PacmanLoader color='white' size={10} />
                    </div>
                  :
                    <div className='icon-span col-sm icon-col'>
                      <RiRobot2Line />
                    </div>
                  }
                  <div className='chat-text-span col-sm text-col'>
                    <MarkdownRenderer content={el.bot}>
                    </MarkdownRenderer>
                    {/*
                    <Markdown remarkPlugins={[remarkGfm]}>
                      {el.bot}
                    </Markdown>
                    */}
                  </div>
                </div>
              </div>
            })}
          </div>
          <div ref={messagesEndRef}></div>
        </div>

        <div className="input-group mb-3 chat-text-input-wrapper">
          <input type="text" className="form-control chat-text-input" placeholder="Ask me something..." aria-describedby="basic-addon1" onChange={(e) => {
            setCurrentInput(e.target.value);
          }} onKeyDown={(e) => {
            if (e.key == "Enter"){
              postQuery();
            }
          }} value={currentInput} />
          <button className="btn btn-outline-secondary submit-chat-text-button" type="button" id="button-addon2" onClick={postQuery}>
            <BsArrowRightCircle />
          </button>
        </div>

        <button className='btn btn-outline-danger clear-chat-btn mb-3 clear-chat-btn' onClick={clearChat}>
          Clear Chat
        </button>
    </div>
  )
}

export default ChatInterface
