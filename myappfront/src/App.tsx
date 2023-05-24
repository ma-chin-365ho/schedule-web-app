import React, { useState } from 'react';

import Toast from 'react-bootstrap/Toast';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import Card from 'react-bootstrap/Card';

import Calendar from 'react-calendar';

import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'react-calendar/dist/Calendar.css';

const ExampleToast = ({ children } : { children : any }) => {
  const [show, toggleShow] = useState(true);

  return (
    <>
      {!show && <Button onClick={() => toggleShow(true)}>Show Toast</Button>}
      <Toast show={show} onClose={() => toggleShow(false)}>
        <Toast.Header>
          <strong className="mr-auto">React-Bootstrap</strong>
        </Toast.Header>
        <Toast.Body>{children}</Toast.Body>
      </Toast>
    </>
  );
};

const TextExample = () => {
  return (
    <Card style={{ width: '18rem' }}>
      <Card.Body>
        <Card.Text>
          Some quick example text to build on the card title and make up the
          bulk of the card's content.
        </Card.Text>
        <Card.Link href="#">Card Link</Card.Link>
      </Card.Body>
    </Card>
  );
};

const NoAnimationExample = () => {
  return (
    <Tabs
      defaultActiveKey="home"
      transition={false}
      id="noanim-tab-example"
      className="mb-3"
    >
      <Tab eventKey="home" title="Home">
        <Container>
          <Row>
            <Col>
              <TextExample />
            </Col>
            <Col>
              <TextExample />
            </Col>
            <Col>
              <TextExample />
            </Col>
          </Row>
        </Container>        
      </Tab>
      <Tab eventKey="profile" title="Profile">
        profile
      </Tab>
      <Tab eventKey="contact" title="Contact" disabled>
        contact
      </Tab>
    </Tabs>
  );
};

const App = () => {

  return (
    <>
      <Calendar  />
      <Container className="p-3">
        <Container className="p-5 mb-4 bg-light rounded-3">
          <h1 className="header">Welcome To React-Bootstrap</h1>
          <ExampleToast>
            We now have Toasts
            <span role="img" aria-label="tada">
              🎉
            </span>
          </ExampleToast>
        </Container>
      </Container>
      <NoAnimationExample />
    </>
  );
};

export default App;
