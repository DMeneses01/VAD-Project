import React from 'react'
import { BrowserRouter as Router, Routes, Route} from "react-router-dom";

import './App.css'

import {Homepage} from "./components/homepage"
import {Dashboard} from "./components/dashboard"
import {By_country} from "./components/by_country"
import {By_sport} from "./components/by_sport"

import {
  HOMEPAGE,
  DASHBOARD,
  BY_COUNTRY,
  BY_SPORT
} from "./urls.js";

const App = () => {
  return (
    <Router>
        <Routes>
          <Route exact path={HOMEPAGE} element={<Homepage />} />
          <Route exact path={DASHBOARD} element={<Dashboard />} />
          <Route exact path={BY_COUNTRY} element={<By_country />} />
          <Route exact path={BY_SPORT} element={<By_sport />} />
        </Routes>
      </Router>
  )
}

export default App