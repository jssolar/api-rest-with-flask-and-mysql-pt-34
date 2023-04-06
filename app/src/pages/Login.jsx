import React, { useContext, useEffect } from 'react'
import { Context } from '../store/AppContext'
import { useNavigate } from 'react-router-dom';
import Alert from '../components/Alert';

const Login = () => {
    const { store: { error, currentUser }, actions } = useContext(Context);
    const navigate = useNavigate();


    useEffect(() => {
        if(currentUser !== null) navigate('/')
    }, [])

    return (
        <div className="container">
            <div className="row">
                <div className="col-md-12">
                    {
                        !!error && (
                            <Alert color={"danger"} text={error.msg} className={""} />
                        )
                    }
                    <form className="form w-50 mx-auto bg-secondary shadow my-5 p-2" onSubmit={(e) => actions.login(e, navigate)}>
                        <div className="form-group mb-3">
                            <label htmlFor="username" className="form-label">Username</label>
                            <input type="email" name="email" id="username" className="form-control" placeholder='john.doe@gmail.com' />
                        </div>

                        <div className="form-group mb-3">
                            <label htmlFor="password" className="form-label">Password</label>
                            <input type="password" name="password" id="password" className="form-control" placeholder='********' />
                        </div>
                        <button className="btn btn-primary btn-sm py-2 w-100">Login</button>
                    </form>
                </div>
            </div>
        </div>
    )
}

export default Login