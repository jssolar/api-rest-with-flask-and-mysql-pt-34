import React, { useContext } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import NotFound from './pages/NotFound'
import Home from './pages/Home'
import Login from './pages/Login'
import Register from './pages/Register'
import Navbar from './components/Navbar'
import ProtectedRoute from './utils/ProtectedRoute'
import injectContext, { Context } from './store/AppContext'

const App = () => {
    const { store: { currentUser } } = useContext(Context);
    return (
        <BrowserRouter>
            <Navbar />
            <Routes>
                <Route path='/register' element={<Register />} />
                <Route path='/login' element={<Login />} />
                <Route path='/' element={<ProtectedRoute currentUser={currentUser}><Home /></ProtectedRoute>} />
                <Route path='*' element={<NotFound />} />
            </Routes>
        </BrowserRouter>
    )
}

export default injectContext(App)