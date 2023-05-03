import React, { useState, useEffect } from "react";
import './styles/homepage.css';
import Olympic from "./data/olympic-rings.png";
import GitHub from "./data/github.png";
import Seta from "./data/round-chevron-right.svg"
import { DASHBOARD } from "../urls";
import { useNavigate } from "react-router-dom";

export const Homepage = () => {

    let navigate = useNavigate();

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
                    <text id='name' style={{width: '20vw', top: '6vh'}}>Duarte Meneses</text>
                    <text id='name' style={{width: '20vw', top: '10vh'}}>Patricia Costa</text>
                    <text id='number' style={{width: '20vw', top: '6vh'}}>2019216949</text>
                    <text id='number' style={{width: '20vw', top: '10vh'}}>2019213995</text>
                    <text id='number' style={{left:'6vw' ,width: '20vw', top: '15vh'}}>2022/2023</text>
                </div>

                <div id='sg2'> 
                    <text id='profile' style={{width: '20vw', height: '2vh', left: '7vw', top: '4vh'}}>Profile</text>
                    <img id='git' src={GitHub} />
                    <text id='profile' style={{width: '20vw', height: '2vh', left: '8vw', top: '12.5vh'}}>GitHub</text>
                    <a id='profile' style={{width: '20vw', height: '2vh', left: '5vw', top: '21vh'}} href="https://github.com/DMeneses01">@DMeneses01</a>
                    <a id='profile' style={{width: '20vw', height: '2vh', left: '7vw', top: '27vh'}} href="https://github.com/patii01">@patii01</a>
                </div>

                <div id='front_button'>
                    <button id='buttonNext' type='button' onClick={() => {navigate(DASHBOARD)}} >Next</button>
                    <img id='seta' src={Seta} />
                </div>
                

            </div>

        </div>
    )
}