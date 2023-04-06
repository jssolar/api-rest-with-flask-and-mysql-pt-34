import React from 'react'
import { Navigate } from 'react-router-dom'

const ProtectedRoute = ({ currentUser, children }) => {
    if (!currentUser) {
        return <Navigate to='/login' replace />
    }
    return children
}

export default ProtectedRoute