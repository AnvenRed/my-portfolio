import React from 'react';
import { shallow } from 'enzyme';
import ExampleWorkModal from '../js/example-work-modal';

import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
Enzyme.configure({ adapter : new Adapter() });

const myExample = {
    'title': "Portfolio Boilerplate",
    'desc': "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    'href': "https://example.com",
    'image': {
      'desc': "A Serverless Portfolio",
      'src': "images/example1.png",
      'comment': ""
    }
  };

describe("Testing ExampleWorkModal Component", () => {
  let component = shallow(<ExampleWorkModal example={myExample} open={false}/>);
  let componentOpen = shallow(<ExampleWorkModal example={myExample} open={true}/>);
  let anchors = component.find("a");

  it("Should contain a single 'a' element", () => {
    expect(anchors.length).toEqual(1);
  });

  it("Should link to the right project", () => {
    expect(anchors.prop('href')).toEqual(myExample.href);
  });

  it("Should have the modalClass set correctly", () => {
    expect(component.find(".background--skyBlue").hasClass("modal--closed")).toBe(true);
    expect(componentOpen.find(".background--skyBlue").hasClass("modal--open")).toBe(true);
  });
});
