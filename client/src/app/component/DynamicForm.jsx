'use client'
import React, {useState} from 'react'
import { useDispatch } from 'react-redux'
import {addForm} from '../../store/formSlice'

const Home = () => {

    const dispatch = useDispatch()

    const [title, setTitle] = useState('')
    const [description, setDescription] = useState('')
    const [type, setType] = useState('')
    const [require, setRequire] = useState(false)

    // const [formData, setFormData] = useState({
    //   title: title,
    //   description: description,
    //   type: type,
    //   require: require
    // })

    const AddData = () => {

      const formData = {
        title: title,
        description: description,
        type: type,
        require: require
      }

      dispatch(addForm(formData))
      setTitle('')
      setDescription('')
      setType('')
      setRequire(false)
    }

  return (
    <main className='container mx-auto my-28 max-w-[500px] border-[#f3f2f2] border-[1px] shadow-lg p-8 flex flex-col'>
    <h1 className=' text-xl text-center font-bold p-4 text-blue-500'>Custom Form</h1>
    <div role='form' className='flex flex-col max-w-[500px]'>
      <label htmlFor='matricno'>Form Title</label>
      <input 
        className=' outline-none p-2 bg-[#ccc] rounded-sm my-2' 
        type='text' placeholder='Form Title' id='title'
        onChange={(ttl) => setTitle(ttl.target.value)}/>
      <label htmlFor="type">Select type</label>
      <select name="type" id="type" className='my-2 outline-none w-52'
        onChange={(typ) => setType(typ.target.value)}>
        <option defaultValue={''}>Select type</option>
        <option value="email">email</option>
        <option value="text">text</option>
        <option value="file">file</option>
        <option value="checkbox">checkbox</option>
        <option value="radio">radio</option>
        <option value="date">date</option>
      </select>
      <div className='flex flex-row'>
        <label htmlFor="require">require</label>
        <input type="radio" id='require' className='my-2 outline-none w-52' 
          onChange={(req) => setRequire(req.target.value)}
        />
      </div>
      <button className='mt-10 px-4 py-2 mx-auto text-white bg-blue-500 items-center flex flex-row justify-center rounded-md' onClick={AddData}>Add form</button>
    </div>
    <section>
      <h1>Forms</h1>



    </section>
</main> 
  )
}

export default DynamicForm