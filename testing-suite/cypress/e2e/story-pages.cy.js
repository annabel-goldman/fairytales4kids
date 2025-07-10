describe('Story Pages', () => {
  it('should load the stories listing page', () => {
    cy.visit('/pages/stories.html')
    
    // Check if page loads
    cy.get('body').should('be.visible')
    cy.get('h1').should('contain', 'Welcome to Fairytales 4 Kids')
    
    // Check for story cards
    cy.get('.story-card').should('exist')
    cy.get('.story-card').should('have.length.greaterThan', 0)
  })

  it('should have working story links', () => {
    cy.visit('/pages/stories.html')
    
    // Check that story cards have proper links
    cy.get('.story-card').first().should('have.attr', 'href')
    
    // Test that at least one story link works
    cy.get('.story-card').first().click()
    cy.url().should('include', '.html')
  })

  it('should load a specific story page', () => {
    // Test with a story that's likely to exist
    cy.visit('/pages/stories/little-red-riding-hood.html')
    
    // Basic checks for story content
    cy.get('body').should('be.visible')
    cy.get('h1, h2, h3').should('exist')
    cy.get('p').should('exist')
  })
}) 