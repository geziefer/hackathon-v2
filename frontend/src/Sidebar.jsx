import React from 'react'
import './static/css/sidebar.css'
import img from './static/imgs/valantic-logo-white-small.png'


const Sidebar = () => {
  return (
    <div id='sidebar'>
        <img src={img} className='sidebar-header-img' />
        <div className='sidebar-text-wrapper'>
            <p className='placeholder-sidebar-text'>
              [HACKATHON-MODE]<br/>
              Only 1 active Chat
            </p>
        </div>
    </div>
  )
}

export default Sidebar
/* TEST */
