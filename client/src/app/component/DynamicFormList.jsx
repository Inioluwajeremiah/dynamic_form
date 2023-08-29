'use client'
import React, { useState } from 'react'

const DynamicFormList = () => {

  const [formContent, setFormCOntent] = useState([])
  const [onEdit, setOnEdit] = useState(false)
  const [textField, setTextField] = useState('')
  const [editedField, setEditedField] = useState('')
  const [title, setTitle] = useState('')

  const AddQUesstion = () => {

    const field = {
      'name': `question_${formContent.length}`,
      'label': 'untitled question',
      'type': 'short_text',
      'list': []
    }
    setFormCOntent([...formContent, field])
  }

  const editFieldLabel = (fieldName, fieldLabel) => {
    const formFields = [...formContent]
    const fieldIndex = formFields.findIndex((item) => item.name === fieldName)
    if (fieldIndex > -1) {
      formFields[fieldIndex].label = fieldLabel
      setFormCOntent(formFields)
    }
  }

  const editFieldType = (fieldName, fieldLabel) => {
    const formFields = [...formContent]
    const fieldIndex = formFields.findIndex((item) => item.name === fieldName)
    if (fieldIndex > -1) {
      formFields[fieldIndex].type = fieldLabel
      setFormCOntent(formFields)
    }
  }

  const AddMultipleChoiceOptions = (fieldName, option) => {
    const formFields = [...formContent]
    const fieldIndex = formFields.findIndex((item) => item.name === fieldName)
    if (fieldIndex > -1) {
      if (option && option != "") {
        formFields[fieldIndex].list.push (option)
        setFormCOntent(formFields)
        setTextField("")
      }
    }
  }

  const SubmitForm = () => {
    const url = ''
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': application/json
      },
      body: {
        title: title,
        content: formContent,
        date: new Date.now()
      }
    })
  }

  return (
    <main className='my-12 mx-auto max-w-[500px] border-[1px] p-4 border-[#ddd]'>
      <div className='flex flex-row justify-between border-b-[1px] border-[#ddd] p-4'>
        <h1 className=' my-4 text-2xl font-bold'>Form</h1>
        <button className='bg-green-500 px-2 py-1 rounded-sm text-white'>Save Form</button>
      </div>
      <div>
        {
          formContent.map((field, index)  => 
          <div key={index} className='mx-auto max-w-[500px] border-[1px] p-4 border-[#ddd]'>
            <div className='flex flex-row justify-between'>
              {
                onEdit && editedField == field.name ? 
                <input type="text" placeholder={field.label} className='border-[1px] border-[#ddd] my-2 outline-none p-2' 
                onChange={(evt) => editFieldLabel(field.name, evt.target.value)} 
                onBlur={() => {setOnEdit(false); setEditedField("")}}/> :
                <label htmlFor="" className='my-4' onClick={() => {setOnEdit(true); setEditedField(field.name)}}>
                  {field.label}</label>
              }
              <select name="" id="" onChange={(evt) => editFieldType(field.name, evt.target.value)}>
                <option value="email">Email</option>
                <option value="short_text">Short Text</option>
                <option value="short_number">Short Number</option>
                <option value="multiline_text">Multiline Text</option>
                <option value="multiple_choice">Multiple Choice</option>
              </select>
            </div>

            <div>
              
              {
                field.type == "short_text" && <input type="text" className='w-full p-4 border-[1px] border-[#ddd] outline-none' placeholder={field.label} />
              }

              {
                field.type == "short_number" && <input type="number" className='w-full p-4 border-[1px] border-[#ddd] outline-none' placeholder={field.label} />
              }
              {
                field.type == "email" && <input type="email" className='w-full border-[1px] p-4 border-[#ddd] outline-none' placeholder={field.label} />
              }
              {
                field.type == "multiline_text" && <textarea name="" id="" cols="30" rows="10" className='p-4 border-[1px] border-[#ddd] w-full outline-none'></textarea>
              }
              {
                  field.type == "multiple_choice" && 
                    <div className='flex flex-col space-y-2 mt-8'>
                      <select name="" id="" className='border-[1px] p-4 border-[#ddd]'>
                        {
                          field.list.map((item, index) => 
                            <option key={index} value={item} className='border-[1px] p-4 border-[#ddd] '>{item}</option>
                          )
                        }
                      </select>

                    <div  className='my-4'>
                      <input type="text" placeholder='Add an option'className='border-[1px] p-2 border-[#ddd] outline-none mr-4' value={textField} onChange={(evt) => setTextField(evt.target.value)}/>
                      <button className='p-2 bg-sky-500 rounded' onClick={() => AddMultipleChoiceOptions(field.name, textField)}>Add option</button>
                    </div>
                  </div>
              }
            </div>
          </div>
          
          )
        }

        <div className='relative w-full p-5 mt-5'>
          <div className='absolute inset-x-0 bottom-0 h-12 flex justify-center'>
            <button className='bg-blue-500 p-4' onClick={() => AddQUesstion()}>Add Form</button>
          </div>
        </div>
      </div>

      <h1 className='text-center pt-16 pb-4'>Form Preview</h1>
      <div>
        {
          formContent.map((field, index)  => 
          <div key={index} >
            <div className='flex flex-row justify-between'>
               
            <label htmlFor="" className='my-4' onClick={() => setOnEdit(true)}>{field.label}</label>
              
            </div>

            <div>
              
              {
                field.type == "short_text" && <input type="text" className='w-full p-4 border-[1px] border-[#ddd]' placeholder={field.label} />
              }

              {
                field.type == "short_number" && <input type="number" className='w-full p-4 border-[1px] border-[#ddd]' placeholder={field.label} />
              }
              {
                field.type == "email" && <input type="email" className='w-full border-[1px] p-4 border-[#ddd]' placeholder={field.label} />
              }
              {
                field.type == "multiline_text" && <textarea name="" id="" cols="30" rows="10" className='p-4 border-[1px] border-[#ddd] w-full my-2'></textarea>
              }
              {
                field.type =="multiple_choice" && <select name="" id="">
                {
                  field.list.map((item, index) =>  
                
                      <option key={index} value={item} className=' border-[1px] p-4 border-[#ddd] outline-none'>{item}</option>
                  )
                }
               
                </select>
              }
            </div>
          </div>
          
          )
        }
      </div>
    </main>
  )
}

export default DynamicFormList