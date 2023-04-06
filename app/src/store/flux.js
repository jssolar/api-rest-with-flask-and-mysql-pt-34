const getState = ({ getStore, getActions, setStore }) => {
    return {
        store: {
            API_URL: 'https://5000-ljavierrodr-apirestwith-ulj5gjltjon.ws-us93.gitpod.io',
            currentUser: null,
            error: null,
            users: null,
            messages: null
        },
        actions: {
            register: async (e, navigate) => {
                e.preventDefault()
                try {
                    const { API_URL } = getStore()
                    const { username, password, role } = e.target;
                    const credentials = { username: username.value, password: password.value, roles: [role.value] }

                    const options = {
                        method: 'POST',
                        body: JSON.stringify(credentials),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }

                    const response = await fetch(`${API_URL}/register`, options)
                    const data = await response.json()

                    if(data.msg){
                        setStore({
                            currentUser: null,
                            error: data
                        })
                    } else {
                        setStore({
                            currentUser: data,
                            error: null
                        })
                        sessionStorage.setItem('currentUser', JSON.stringify(data))
                        navigate('/')
                    }

                } catch (error) {
                    console.log(error.message)
                }
            },
            login: async (e, navigate) => {
                e.preventDefault()
                try {
                    const { API_URL } = getStore()
                    const { username, password } = e.target;
                    const credentials = { username: username.value, password: password.value }

                    const options = {
                        method: 'POST',
                        body: JSON.stringify(credentials),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    }

                    const response = await fetch(`${API_URL}/login`, options)
                    const data = await response.json()

                    if(data.msg){
                        setStore({
                            currentUser: null,
                            error: data
                        })
                    } else {
                        setStore({
                            currentUser: data,
                            error: null
                        })
                        sessionStorage.setItem('currentUser', JSON.stringify(data))
                        navigate('/')
                    }

                } catch (error) {
                    console.log(error.message)
                }
            },
            logout: () => {
                if(sessionStorage.getItem('currentUser')){
                    setStore({
                        currentUser: null
                    })
                    sessionStorage.removeItem('currentUser')
                }
            },
            checkCurrentUser: () => {
                if(sessionStorage.getItem('currentUser')){
                    setStore({
                        currentUser: JSON.parse(sessionStorage.getItem('currentUser'))
                    })
                }
            },
            getUsers: async () => {
                try {
                    const { currentUser, API_URL } = getStore()
                    const options = {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${currentUser?.access_token}`
                        }
                    }
                    const response = await fetch(`${API_URL}/users`, options)
                    const data = await response.json();

                    setStore({
                        users: data
                    })

                } catch (error) {
                    
                }
            },
            getMessages: async () => {
                try {
                    const { currentUser, API_URL } = getStore()
                    const options = {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${currentUser?.access_token}`
                        }
                    }
                    const response = await fetch(`${API_URL}/messages`, options)
                    const data = await response.json();

                    setStore({
                        messages: data
                    })

                } catch (error) {
                    
                }
            }
        }
    }
}

export default getState;