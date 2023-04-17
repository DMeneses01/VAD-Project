import React, { useState, useEffect } from "react";
import './styles/homepage.css';
import Olympic from "./data/olympic-rings.png";

export const Homepage = () => {
    return (
        <div id='body_homepage'>
            <text id='cadeira'>Advanced Data Visualization</text>
            <div id='main_graph'> 
                <img id='symbol' src={Olympic} />
                <text id='title'>Project Name</text>
            </div>
            
            <div id='side_bar'> 
                <text id='authors'>Authors</text>
                <div id='sg1'>
                    <text id='made'>Made by</text>
                </div>
            </div>

        </div>
    )
}