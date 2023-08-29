'use client';

import store from './store'
import { Provider } from 'react-redux/es/exports'

const FormProvider = ({children}) => {
    return <Provider store={store}>
        {children}
    </Provider>
}
export default FormProvider


