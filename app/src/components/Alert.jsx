import React from 'react'

const Alert = ({ text, className, color }) => {
    return (
        <div className={`alert alert-${color} alert-dismissible fade show ${className}`} role="alert">
            {text}
            <button type="button" className="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    )
}

export default Alert