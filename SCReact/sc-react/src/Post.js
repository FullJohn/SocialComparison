import React, {Component} from 'react';
import {Table} from 'react-bootstrap';

export class Post extends Component{
    
    constructor(props){
        super(props);
        this.state={posts:[]}
    }

    refreshList(){
        fetch('http://127.0.0.1:8000/post/')
        .then(response=>response.json())
        .then(data=>{
            this.setState({posts:data});
        });
    }

    componentDidMount(){
        this.refreshList();
    }

    componentDidUpdate(){
        this.refreshList();
    }

    render(){
        const {posts} = this.state;
        return(
            <div>
                <Table className="mt-4" striped bordered hover size="sm">
                    <thead>
                        <tr>
                            <th>PostId</th>
                            <th>url</th>
                            <th>title</th>
                            <th>description</th>
                            <th>thumbnail</th>
                            <th>channel</th>
                            <th>date</th>
                            <th>views</th>
                            <th>comments</th>
                            <th>likes</th>
                        </tr>
                    </thead>
                    <tbody>
                        {posts.map(post=>
                            <tr key={post.PostId}>
                                <td>{post.PostId}</td>
                                <td>{post.url}</td>
                                <td>{post.title}</td>
                                <td>{post.description}</td>
                                <td>{post.thumbnail}</td>
                                <td>{post.channel}</td>
                                <td>{post.date}</td>
                                <td>{post.views}</td>
                                <td>{post.comments}</td>
                                <td>{post.likes}</td>
                            </tr>)}
                    </tbody>


                </Table>
            </div>

        )
    }
}